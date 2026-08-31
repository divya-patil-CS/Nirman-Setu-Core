from google import genai
from google.genai import errors
import json
import os
from dotenv import load_dotenv
from .conversation_prompts import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.6-flash"
REQUIRED_FIELDS = ["name", "gender", "age", "date_of_birth", "occupation", "annual_income"]
MAX_HISTORY_MESSAGES = 10  # keep prompt size manageable


def is_profile_complete(profile: dict) -> bool:
    return all(profile.get(field) for field in REQUIRED_FIELDS)


def format_history(history: list) -> str:
    if not history:
        return "(no previous messages)"
    trimmed = history[-MAX_HISTORY_MESSAGES:]
    lines = [f"{turn['role']}: {turn['text']}" for turn in trimmed]
    return "\n".join(lines)


def chat_step(user_message: str, current_profile: dict, history: list = None, language: str = "Hindi") -> dict:
    history = history or []

    prompt = SYSTEM_PROMPT.format(
        language=language,
        current_profile=json.dumps(current_profile),
        conversation_history=format_history(history)
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"{prompt}\n\nUser: {user_message}"
        )
    except errors.ClientError as e:
        return _error_response(current_profile, history, user_message,
                                "Server is busy right now, please try again in a moment.", str(e))
    except Exception as e:
        return _error_response(current_profile, history, user_message,
                                "Something went wrong. Please try again.", str(e))

    raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        return _error_response(current_profile, history, user_message,
                                "Sorry, I didn't understand that. Could you repeat?", "json_decode_error")

    updated_profile = dict(current_profile)
    new_fields = parsed.get("updated_fields", {})

    # family_members should ADD to the list, not overwrite it
    if "family_members" in new_fields:
        existing_members = updated_profile.get("family_members", [])
        incoming = new_fields.pop("family_members")
        if isinstance(incoming, list):
            existing_members.extend(incoming)
        updated_profile["family_members"] = existing_members

    updated_profile.update(new_fields)

    new_history = history + [
        {"role": "user", "text": user_message},
        {"role": "bot", "text": parsed["reply"]}
    ]

    return {
        "reply": parsed["reply"],
        "profile": updated_profile,
        "profile_complete": is_profile_complete(updated_profile),
        "history": new_history
    }


def _error_response(profile, history, user_message, message, error_detail):
    new_history = history + [
        {"role": "user", "text": user_message},
        {"role": "bot", "text": message}
    ]
    return {
        "reply": message,
        "profile": profile,
        "profile_complete": is_profile_complete(profile),
        "history": new_history,
        "error": error_detail
    }