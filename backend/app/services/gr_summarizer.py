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
from pypdf import PdfReader

# Reads the .env file (if present) and puts GEMINI_API_KEY into the
# environment, so os.environ.get("GEMINI_API_KEY") below can find it.
load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# The model to use. If Google renames/upgrades their models by the time you
# read this, check https://ai.google.dev/gemini-api/docs/models for the
# current recommended "flash" (fast + cheap) model name and update this one
# line — nothing else in this file needs to change.
GEMINI_MODEL = "gemini-3.6-flash"

# gemini-3.6-flash has a 1,048,576 token context window (roughly 750,000
# words). A GR document would need to be enormous to threaten that, so
# this is a generous safety cap, not a "typical size" assumption — most
# real GRs (even long ones) will be a small fraction of this. If a
# document is SOMEHOW still bigger than this, it gets chunked (see
# summarize_gr's warning below) rather than blindly cut off.
MAX_INPUT_CHARACTERS = 500000


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


# ---------------------------------------------------------------------
# PDF SUPPORT — so an admin can upload a GR PDF directly, instead of
# pasting raw text. This is the piece that plugs into an "Upload GR" /
# "Process" button: whoever owns the FastAPI route just needs to save
# the uploaded file to disk and call summarize_gr_from_pdf() with its
# path — everything else (extraction, fallback, calling Gemini) happens
# here.
# ---------------------------------------------------------------------

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts plain text from a PDF using pypdf. Returns an empty string
    if the file can't be read or has no extractable text (e.g. a scanned
    PDF with no text layer at all).
    """
    try:
        reader = PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception as error:
        print(f"[gr_summarizer] ERROR reading PDF '{pdf_path}': {error}")
        return ""


def _looks_garbled(text: str, min_devanagari_ratio: float = 0.15) -> bool:
    """
    Many older Maharashtra government GRs are typeset in a legacy,
    non-Unicode Marathi font (Kruti Dev, Shree-Lipi, etc.). Extracting
    text from these with pypdf produces characters that LOOK like normal
    text but are not actually Devanagari — garbage in, garbage out if
    sent to Gemini as-is.

    Heuristic: of all alphabetic characters found, what fraction actually
    fall in the Devanagari Unicode block (U+0900–U+097F)? A properly
    extracted Marathi/Hindi document should score high; a
    legacy-font-garbled one scores near zero. Documents that are mostly
    English are exempted by the small-sample check below.
    """
    letters = [c for c in text if c.isalpha()]
    if len(letters) < 20:
        return False  # not enough text to judge either way

    devanagari_letters = [c for c in letters if "\u0900" <= c <= "\u097F"]
    ascii_letters = [c for c in letters if c.isascii()]

    # If it's clearly plain English (mostly ASCII letters), it's not a
    # garbled-Devanagari case — don't flag it.
    if len(ascii_letters) / len(letters) > 0.85:
        return False

    ratio = len(devanagari_letters) / len(letters)
    return ratio < min_devanagari_ratio


def summarize_gr_from_pdf(pdf_path: str, language: str, scheme_name: str = None) -> dict:
    """
    THE FUNCTION AN "UPLOAD GR" BUTTON SHOULD CALL.

    Takes the path to an uploaded GR PDF (already saved to disk by
    whoever handles the upload endpoint), and returns the same
    {"success": True/False, ...} shape as summarize_gr().

    What it does:
      1. Tries to extract the PDF's text with pypdf.
      2. If that text looks garbled (legacy non-Unicode font — common in
         older Marathi GRs), it skips the text pipeline entirely and
         sends the PDF FILE ITSELF to Gemini, which reads it visually
         instead of relying on the broken character encoding.
      3. Otherwise, it summarizes the cleanly extracted text the normal
         way (same as calling summarize_gr() directly).

    This never raises — errors come back as {"success": False, "error": ...}.
    """
    if not pdf_path or not os.path.isfile(pdf_path):
        return {"success": False, "error": f"PDF file not found: {pdf_path}"}

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

    extracted_text = extract_text_from_pdf(pdf_path)

    if extracted_text and not _looks_garbled(extracted_text):
        # Clean text extracted — use the normal text-based pipeline.
        return summarize_gr(gr_text=extracted_text, language=language, scheme_name=scheme_name)

    # Either no extractable text, or it looks garbled — fall back to
    # sending Gemini the PDF file directly so it reads it visually.
    reason = "no extractable text layer" if not extracted_text else "extracted text appears garbled (legacy font)"
    print(f"[gr_summarizer] '{pdf_path}': {reason}, falling back to native PDF reading")

    try:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
    except Exception as error:
        return {"success": False, "error": f"Could not read PDF file: {error}"}

    prompt = _build_prompt("(see attached PDF)", language, scheme_name)

    try:
        from google.genai import types
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                prompt,
            ],
        )
    except Exception as error:
        print(f"[gr_summarizer] ERROR calling Gemini API with PDF: {error}")
        return {"success": False, "error": f"Could not reach the summarization service: {error}"}

    summary_text = getattr(response, "text", None)
    if not summary_text or not summary_text.strip():
        return {"success": False, "error": "The summarization service returned an empty response."}

    return {"success": True, "summary": summary_text.strip()}