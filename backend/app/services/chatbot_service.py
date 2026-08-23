from google import genai
import json
import os
from dotenv import load_dotenv
from .conversation_prompts import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.6-flash"

REQUIRED_FIELDS = ["name", "age", "date_of_birth", "occupation"]


def is_profile_complete(profile: dict) -> bool:
    return all(profile.get(field) for field in REQUIRED_FIELDS)


def chat_step(user_message: str, current_profile: dict, language: str = "Hindi") -> dict:
    prompt = SYSTEM_PROMPT.format(
        language=language,
        current_profile=json.dumps(current_profile)
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"{prompt}\n\nUser: {user_message}"
    )

    raw_text = response.text.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "reply": "Sorry, I didn't understand that. Could you repeat?",
            "profile": current_profile,
            "profile_complete": is_profile_complete(current_profile)
        }

    updated_profile = {**current_profile, **parsed.get("updated_fields", {})}

    return {
        "reply": parsed["reply"],
        "profile": updated_profile,
        "profile_complete": is_profile_complete(updated_profile)
    }