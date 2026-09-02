"""
gr_summarizer.py
===================

WHAT THIS FILE DOES:
  Takes the raw text of a Government Resolution (GR) document for a scheme,
  and asks Google's Gemini model to turn it into a short, simple, plain-
  language summary — covering what the benefit is, who qualifies, and what
  documents are needed — written in whatever regional language the user
  picked.

  Think of this as handing a dense legal document to a friendly translator
  who reads it once and explains it to you in one paragraph, in your own
  language, with no legal jargon.

SETUP YOU NEED TO DO BEFORE THIS WORKS:
  1. Install the package:
        pip install google-genai
  2. Get a Gemini API key from https://aistudio.google.com/apikey
  3. DO NOT paste your API key directly into this file. Instead, set it as
     an environment variable called GEMINI_API_KEY. The easiest way for a
     hackathon:
        - Create a file called ".env" in your backend/ folder (same folder
          you run commands from) with one line:
              GEMINI_API_KEY=your_actual_key_here
        - Add ".env" to your .gitignore file so it never gets pushed to
          GitHub (an API key in a public repo can be stolen and abused).
        - Install python-dotenv: pip install python-dotenv
        - This file loads that .env automatically (see load_dotenv() below).
"""

import os
from google import genai
from dotenv import load_dotenv

# Reads the .env file (if present) and puts GEMINI_API_KEY into the
# environment, so os.environ.get("GEMINI_API_KEY") below can find it.
load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# The model to use. If Google renames/upgrades their models by the time you
# read this, check https://ai.google.dev/gemini-api/docs/models for the
# current recommended "flash" (fast + cheap) model name and update this one
# line — nothing else in this file needs to change.
GEMINI_MODEL = "gemini-3.6-flash"

# A GR document could theoretically be huge. This is a rough safety cap so
# we don't send something absurd to the API and rack up cost/latency. Feel
# free to raise this if your GR documents are long and you need more.
MAX_INPUT_CHARACTERS = 30000


def _build_prompt(gr_text: str, language: str, scheme_name: str = None) -> str:
    """
    Builds the instruction we send to Gemini. Kept as its own function so
    you (or a teammate) can easily tweak the wording later without touching
    the rest of the logic.
    """
    scheme_name_line = f'This document is for the scheme called "{scheme_name}".\n' if scheme_name else ""

    return f"""You are explaining a government scheme to someone with no legal or
government background, in simple {language}.

{scheme_name_line}Below is the raw text of an official Government Resolution (GR) document.
Read it and write a SHORT, SIMPLE summary a common citizen can understand in
under a minute. Do not use legal or bureaucratic jargon. Use short sentences.

Your summary must cover exactly these three things, clearly separated:
1. Benefit: What does the applicant actually get (money, service, subsidy, etc.)?
2. Eligibility criteria: Who can apply, in plain terms?
3. Required documents: What documents/proofs are needed to apply?

If any of these three things is not mentioned in the document, say so plainly
(e.g. "Not specified in this document") instead of guessing or making
something up.

Write the entire summary in {language}. Keep it concise — a few sentences per
section is enough.

--- BEGIN GR DOCUMENT TEXT ---
{gr_text}
--- END GR DOCUMENT TEXT ---
"""


def summarize_gr(gr_text: str, language: str, scheme_name: str = None) -> dict:
    """
    THE MAIN FUNCTION OF THIS FILE.

    Arguments:
        gr_text      : the raw text of the GR document (a plain string)
        language     : the regional language to write the summary in,
                        e.g. "Hindi", "Marathi", "Tamil", "English"
        scheme_name  : optional — the scheme's name, to give Gemini context

    Returns a dict, always with a "success" key so the caller can check it
    without needing a try/except of their own:

        On success:
            {"success": True, "summary": "..."}

        On failure (empty input, missing API key, network/API error):
            {"success": False, "error": "human-readable reason"}

    This function NEVER raises an exception itself — any problem talking to
    the Gemini API is caught and turned into the {"success": False, ...}
    shape above, so a flaky network connection or a bad API key can't crash
    your FastAPI endpoint.
    """
    # --- Basic input validation, before we spend any API calls ---
    if not gr_text or not gr_text.strip():
        return {"success": False, "error": "No GR text was provided to summarize."}

    if not language or not language.strip():
        return {"success": False, "error": "No target language was specified."}

    if not GEMINI_API_KEY:
        return {
            "success": False,
            "error": (
                "GEMINI_API_KEY is not set. Add it to a .env file in the backend "
                "folder (see the setup instructions at the top of gr_summarizer.py)."
            ),
        }

    text_to_send = gr_text
    if len(gr_text) > MAX_INPUT_CHARACTERS:
        print(
            f"[gr_summarizer] WARNING: GR text is {len(gr_text)} characters, "
            f"truncating to {MAX_INPUT_CHARACTERS} before sending to Gemini."
        )
        text_to_send = gr_text[:MAX_INPUT_CHARACTERS]

    prompt = _build_prompt(text_to_send, language, scheme_name)

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
    except Exception as error:
        # Covers: invalid API key, network problems, rate limits, the
        # service being down, etc. We don't try to guess which one — we
        # just fail safely and tell the caller something went wrong.
        print(f"[gr_summarizer] ERROR calling Gemini API: {error}")
        return {"success": False, "error": f"Could not reach the summarization service: {error}"}

    summary_text = getattr(response, "text", None)
    if not summary_text or not summary_text.strip():
        return {"success": False, "error": "The summarization service returned an empty response."}

    return {"success": True, "summary": summary_text.strip()}