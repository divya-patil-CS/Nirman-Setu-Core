"""
scheme_extractor.py
======================

Takes a GR document (text) and asks Gemini to produce a human-readable
summary AND a structured scheme record in the EXACT SAME shape as the
scheme dicts already in schemes_data.py — so it plugs into
rule_engine.py with ZERO changes to that file.

CRITICAL — validate_schemes() is NOT semantic verification:
  This file runs extracted rules through validate_schemes() (the same
  validator used for hand-written schemes). That ONLY confirms the rule
  is STRUCTURALLY well-formed — right operators, no empty conditions,
  unique scheme_id. It has no way to confirm Gemini actually understood
  the GR correctly (e.g. that an income cutoff is the right number, or
  that a condition should have been OR instead of AND). Every extracted
  scheme is returned with "requires_admin_review": True, always, and
  this is not something a caller can bypass by checking
  validation_errors == [] — passing structural validation and being
  semantically correct are two different things, and only a human
  reading the source GR can confirm the second one.
"""

import os
import json
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.6-flash"

# Gemini's context window (hundreds of thousands to over a million tokens,
# depending on model) comfortably covers any single GR document you're
# likely to encounter — the old 30,000-char limit inherited from
# gr_summarizer.py was needlessly conservative and silently cut real
# documents short (this is what happened with the 45,168-char Bhausaheb
# GR). This limit exists only as a safety net for a truly unusual,
# enormous document. If it IS hit, the document is chunked (see
# _chunk_text / _merge_chunk_results below) rather than truncated.
MAX_INPUT_CHARACTERS = 500000

ALLOWED_OPERATORS = ["==", "!=", "<", "<=", ">", ">=", "in", "not_in"]

KNOWN_PROFILE_FIELDS = [
    "age", "gender", "occupation", "annual_income", "caste",
    "agricultural_land_hectares", "aadhaar_available",
    "bank_account_linked_aadhaar", "beneficiary_type", "division",
    "farm_category", "has_disability", "family_livelihood_only_agriculture",
    "family_members.count", "family_members.has_relation",
    "family_members.min_age", "family_members.max_age",
]

# For fields that take one of a small set of known values, tell Gemini
# the EXACT casing/spelling already used elsewhere in schemes_data.py.
# Without this, Gemini reasonably writes "Konkan" (proper-noun casing,
# grammatically correct) while the actual profile convention is
# lowercase "konkan" — a mismatch validate_schemes() cannot catch,
# because both are structurally valid strings. This happened in a real
# extraction: "division" came back as "Konkan" and would have silently
# failed every real Konkan farmer's eligibility check had it gone live
# unreviewed. _normalize_known_field_values() below is a second,
# code-level safety net for the same problem — this hint reduces how
# often that net needs to catch anything.
KNOWN_FIELD_VALUE_CONVENTIONS = {
    "division": 'lowercase, e.g. "konkan" or "other" — never "Konkan"',
    "beneficiary_type": 'lowercase, e.g. "individual" or "institutional"',
    "gender": 'lowercase, e.g. "male" or "female"',
    "occupation": 'lowercase, e.g. "farmer", "laborer"',
    "caste": 'use the short form as written in the GR, e.g. "SC", "ST", "OBC", "Nav-Buddhist"',
}

# Fields normalized in-place to lowercase after extraction, as a
# code-level backstop independent of whether Gemini followed the hint
# above. Only fields with a small, known, lowercase-by-convention value
# set belong here — never "caste" (short forms like "SC" must stay
# uppercase) or free-text fields.
FIELDS_TO_LOWERCASE = {"division", "beneficiary_type", "gender", "occupation"}


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", name.strip().lower())
    return slug.strip("_")[:80]


def _normalize_known_field_values(rule_node) -> None:
    """
    Walks a rule tree in place and lowercases the value of any leaf
    condition on a field listed in FIELDS_TO_LOWERCASE, when that value
    is a string. This is the code-level backstop for the casing problem
    described above the FIELDS_TO_LOWERCASE definition — it runs
    regardless of whether the prompt hint was followed.
    """
    if not isinstance(rule_node, dict):
        return

    if "conditions" in rule_node:
        for sub_node in rule_node["conditions"]:
            _normalize_known_field_values(sub_node)
    elif "field" in rule_node:
        if rule_node.get("field") in FIELDS_TO_LOWERCASE:
            value = rule_node.get("value")
            if isinstance(value, str):
                rule_node["value"] = value.lower()
            elif isinstance(value, list):
                rule_node["value"] = [v.lower() if isinstance(v, str) else v for v in value]


def find_possible_duplicate_schemes(scheme_name: str, existing_names: list, threshold: float = 0.4) -> list:
    """
    A real problem this catches: this exact Bhausaheb Fundkar scheme
    already exists by hand in schemes_data.py as
    "Bhausaheb Fundkar Falbag Lagvad Yojana" (scheme_id
    "bhausaheb_fundkar_falbag"). Gemini extracting the same GR
    independently named it "Bhausaheb Fundkar Orchard Plantation Scheme"
    — a reasonable English paraphrase, but slugify() turns that into a
    DIFFERENT scheme_id. Approve it as-is and the same real-world scheme
    is live twice under two different IDs.

    Uses word-overlap similarity (shared distinctive words / smaller
    name's word count) rather than character-sequence similarity —
    "Bhausaheb Fundkar Falbag Lagvad Yojana" and "Bhausaheb Fundkar
    Orchard Plantation Scheme" share almost no consecutive characters
    once you get past "Bhausaheb Fundkar", so a character-diff ratio
    (tried first, and it missed this real case) scores them as unrelated
    even though the two most distinctive words — the proper nouns — are
    identical. Word overlap catches that; a plain diff ratio does not.
    """
    matches = []
    new_words = set(re.findall(r"[a-z]+", scheme_name.lower()))

    for existing_name in existing_names:
        existing_words = set(re.findall(r"[a-z]+", existing_name.lower()))
        if not new_words or not existing_words:
            continue
        overlap = new_words & existing_words
        ratio = len(overlap) / min(len(new_words), len(existing_words))
        if ratio >= threshold:
            matches.append({
                "existing_name": existing_name,
                "similarity": round(ratio, 2),
                "shared_words": sorted(overlap),
            })

    return sorted(matches, key=lambda m: -m["similarity"])


def _build_extraction_prompt(gr_text: str, summary_language: str) -> str:
    return f"""You are converting an official Government Resolution (GR) document
into structured data for an eligibility-checking system.

Respond with ONLY a single JSON object. No markdown fences, no preamble,
no explanation outside the JSON.

The JSON object must have exactly these keys:

"scheme_name": the scheme's official name, in English.

"description": a short, simple, plain-language summary in {summary_language},
explaining the benefit, who qualifies, and what documents are needed. No
legal jargon.

"rules": a rule tree using ONLY this shape (nest as needed):
  - a group: {{"operator": "AND" or "OR", "conditions": [ ...more nodes... ]}}
  - a leaf condition: {{"field": "...", "op": "...", "value": ...}}
  Only use these operators in "op": {ALLOWED_OPERATORS}
  Prefer these existing field names when the condition matches one:
  {KNOWN_PROFILE_FIELDS}
  Some fields must use an EXACT value convention already used elsewhere
  in this system — match these exactly, including casing:
  {json.dumps(KNOWN_FIELD_VALUE_CONVENTIONS, indent=2)}
  If a condition needs a field not in that list, still write it as a
  leaf condition with your best short field name — it will be reviewed
  by a human before use, so do not skip a condition just because the
  field is new.
  If you cannot confidently express a rule as a rule, do NOT invent a
  guess — leave it out of "rules" and describe it in "flagged_conditions"
  instead. It is better to under-encode than to silently produce a
  wrong eligibility rule.

"required_documents": a list of short strings naming documents applicants
need.

"benefits": a list of short strings describing what the applicant
receives.

"eligibility_criteria": a list of short, plain-language sentences
describing who qualifies, for a HUMAN reading it on a webpage — e.g.
"Applicant must be an individual farmer", "Land holding must be between
0.10 and 10.00 hectares in Konkan, or 0.20 to 6.00 hectares elsewhere".
This must cover the SAME conditions as "rules" below, just in readable
sentences instead of code — every condition in "rules" should have a
matching plain-language sentence here, and vice versa where possible.

"rules": a rule tree using ONLY this shape (nest as needed) — this is
for the ELIGIBILITY ENGINE, not for display, so it must be exact:
  - a group: {{"operator": "AND" or "OR", "conditions": [ ...more nodes... ]}}
  - a leaf condition: {{"field": "...", "op": "...", "value": ...}}
  Only use these operators in "op": {ALLOWED_OPERATORS}
  Prefer these existing field names when the condition matches one:
  {KNOWN_PROFILE_FIELDS}
  Some fields must use an EXACT value convention already used elsewhere
  in this system — match these exactly, including casing:
  {json.dumps(KNOWN_FIELD_VALUE_CONVENTIONS, indent=2)}
  If a condition needs a field not in that list, still write it as a
  leaf condition with your best short field name — it will be reviewed
  by a human before use, so do not skip a condition just because the
  field is new.
  If you cannot confidently express a rule as a rule, do NOT invent a
  guess — leave it out of "rules" (and out of "eligibility_criteria" as
  a hard requirement) and describe it in "restrictions_and_conditions"
  instead. It is better to under-encode than to silently produce a
  wrong eligibility rule.

"restrictions_and_conditions": a list of short plain-English strings
describing any condition, exception, priority rule, timeline, or
restriction that is NOT a simple pass/fail eligibility check — e.g.
priority/selection factors that don't disqualify anyone, conditions that
depend on a prior benefit in a complex way, survival-rate or maintenance
requirements for continued payment, cross-references to another GR's
paragraphs. Flagging these here is correct behavior, not a failure — do
not omit them to make "rules" or "eligibility_criteria" look complete.

"application_process": a list of short, ordered, plain-language steps
describing how an applicant actually applies (e.g. "Submit application
within 21 days of the advertisement", "Attach required documents",
"Selection by lottery if applications exceed the funded target"). If the
document doesn't describe a process, return an empty list.

"deadline": a date string "YYYY-MM-DD" if stated, or null.

--- BEGIN GR DOCUMENT TEXT ---
{gr_text}
--- END GR DOCUMENT TEXT ---
"""


def _parse_json_response(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned)
    return json.loads(cleaned)


def _call_gemini_for_extraction(text_chunk: str, summary_language: str) -> dict:
    """
    One single Gemini call for one chunk of text. Returns the parsed
    JSON dict (NOT yet wrapped in the scheme_id/active/status shape).
    Raises on failure — callers (extract_scheme / extract_scheme_chunked)
    catch and turn exceptions into {"success": False, ...} responses.
    """
    prompt = _build_extraction_prompt(text_chunk, summary_language)
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)

    raw_text = getattr(response, "text", None)
    if not raw_text or not raw_text.strip():
        raise ValueError("The extraction service returned an empty response.")

    return _parse_json_response(raw_text)


def _chunk_text(text: str, chunk_size: int, overlap: int = 2000) -> list:
    """
    Splits text into overlapping chunks. The overlap exists so a clause
    that happens to sit right at a chunk boundary doesn't get cut in
    half and lost from both chunks.
    """
    if chunk_size <= overlap:
        # Guards against a configuration mistake where chunk_size is not
        # meaningfully larger than overlap — without this, `start` would
        # advance by a tiny amount (or not at all) each iteration,
        # producing an unbounded number of chunks instead of failing
        # loudly. In real use chunk_size is always MAX_INPUT_CHARACTERS
        # (300,000), far bigger than the 2,000-char overlap, so this
        # should never trigger outside of a misconfiguration.
        raise ValueError(
            f"chunk_size ({chunk_size}) must be larger than overlap ({overlap})"
        )

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def _merge_chunk_results(parsed_chunks: list) -> dict:
    """
    Merges the parsed JSON from multiple chunks into one. This is
    deliberately conservative:
      - benefits / required_documents / eligibility_criteria /
        restrictions_and_conditions / application_process are combined
        and de-duplicated (safe — these are just lists of facts).
      - "rules" is NOT merged by guessing how to combine conditions from
        different chunks (e.g. blindly AND-ing them together could
        produce a rule stricter than the actual GR, and OR-ing them
        could produce one looser than intended — both are wrong in
        different ways). Instead, if MORE THAN ONE chunk produced a
        non-empty "rules", this is flagged in "admin_notes" (a
        process/system note, distinct from "restrictions_and_conditions"
        which is GR-sourced content), and only the first non-empty one
        is used as a starting point for the admin to correct.
    """
    merged = {
        "scheme_name": None,
        "description": "",
        "rules": {},
        "required_documents": [],
        "benefits": [],
        "eligibility_criteria": [],
        "restrictions_and_conditions": [],
        "application_process": [],
        "deadline": None,
        "admin_notes": [],
    }

    rules_candidates = []
    descriptions = []

    for chunk_result in parsed_chunks:
        if not merged["scheme_name"] and chunk_result.get("scheme_name"):
            merged["scheme_name"] = chunk_result["scheme_name"]
        if not merged["deadline"] and chunk_result.get("deadline"):
            merged["deadline"] = chunk_result["deadline"]
        if chunk_result.get("description"):
            descriptions.append(chunk_result["description"])

        for list_field in ("required_documents", "benefits", "eligibility_criteria",
                            "restrictions_and_conditions", "application_process"):
            for item in chunk_result.get(list_field, []):
                if item not in merged[list_field]:
                    merged[list_field].append(item)

        chunk_rules = chunk_result.get("rules")
        if chunk_rules:
            rules_candidates.append(chunk_rules)

    # Keep each chunk's description concatenated — the admin will read
    # this during review, and it's better to see everything each chunk
    # understood than to silently drop all but one.
    merged["description"] = "\n\n".join(descriptions)

    if len(rules_candidates) == 1:
        merged["rules"] = rules_candidates[0]
    elif len(rules_candidates) > 1:
        merged["rules"] = rules_candidates[0]
        merged["admin_notes"].append(
            f"This document was split into {len(parsed_chunks)} chunks for extraction, and "
            f"{len(rules_candidates)} of them each produced eligibility rules. Only the first "
            f"is used in 'rules' below — an admin MUST manually check the other chunks' content "
            f"for eligibility conditions that may be missing."
        )
    # If zero chunks produced rules, merged["rules"] stays {} — validate_schemes
    # will correctly flag this as "matches every user" and refuse to pass silently.

    return merged


def extract_scheme(
    gr_text: str,
    summary_language: str = "English",
    existing_scheme_names: list = None,
    source_document: str = None,
) -> dict:
    """
    THE MAIN FUNCTION OF THIS FILE.

    `source_document` is an optional filename/path/identifier for the
    source GR PDF — Gemini has no way to know this (it only sees text),
    so it's attached here from what the caller already knows about the
    file it read. This becomes the scheme's "source_gr_pdf" field.

    Returns, on success:
        {
            "success": True,
            "scheme": {
                # --- explicit fields for the frontend / a human ---
                "scheme_id": ...,                 # auto-generated slug
                "name": ...,                       # 1. Scheme name
                "description": ...,                # 2. Description/summary
                "eligibility_criteria": [...],     # 3. Eligibility, in plain sentences
                "benefits": [...],                 # 4. Benefits
                "required_documents": [...],       # 5. Required documents
                "deadline": ...,                   # 6. Deadline
                "restrictions_and_conditions": [...], # 7. Restrictions/conditions
                "application_process": [...],      # 8. Application process
                "source_gr_pdf": ...,              # 9. Source GR PDF
                # --- fields for the ELIGIBILITY ENGINE, not display ---
                "rules": {...},                    # what evaluate_rule() reads
                # --- process/workflow fields ---
                "active": False,                   # always False here
                "status": "pending_review",
                "requires_admin_review": True,     # always True, unconditionally
                "admin_notes": [...],               # system-generated review flags
                                                     # (duplicate warnings, multi-chunk
                                                     # merge conflicts) — NOT GR content,
                                                     # not meant for end-user display
            },
            "validation_errors": [...],   <- STRUCTURAL checks only (see
                                              validate_schemes.py's docstring).
                                              Empty here means "rules is
                                              well-FORMED", never "Gemini
                                              understood the GR correctly."
            "possible_duplicates": [...],
        }
    or {"success": False, "error": "..."} on failure. Never raises.

    Documents longer than MAX_INPUT_CHARACTERS are automatically split
    into overlapping chunks and extracted separately (see
    _chunk_text / _merge_chunk_results) rather than being silently cut
    off at the limit.
    """
    if not gr_text or not gr_text.strip():
        return {"success": False, "error": "No GR text was provided to extract from."}

    if not GEMINI_API_KEY:
        return {"success": False, "error": "GEMINI_API_KEY is not set. Add it to your .env file."}

    try:
        if len(gr_text) <= MAX_INPUT_CHARACTERS:
            parsed = _call_gemini_for_extraction(gr_text, summary_language)
            parsed.setdefault("admin_notes", [])
        else:
            chunks = _chunk_text(gr_text, chunk_size=MAX_INPUT_CHARACTERS)
            print(f"[scheme_extractor] Document is {len(gr_text)} chars — "
                  f"splitting into {len(chunks)} chunks for extraction.")
            parsed_chunks = [_call_gemini_for_extraction(c, summary_language) for c in chunks]
            parsed = _merge_chunk_results(parsed_chunks)
    except json.JSONDecodeError as error:
        print(f"[scheme_extractor] ERROR parsing JSON: {error}")
        return {"success": False, "error": f"Could not parse structured data from the model's response: {error}"}
    except Exception as error:
        print(f"[scheme_extractor] ERROR calling Gemini API: {error}")
        return {"success": False, "error": f"Could not reach the extraction service: {error}"}

    scheme_name = parsed.get("scheme_name") or "Unnamed Scheme"

    rules = parsed.get("rules", {})
    _normalize_known_field_values(rules)  # fixes "Konkan" -> "konkan", etc. in place

    admin_notes = list(parsed.get("admin_notes", []))

    scheme = {
        "scheme_id": _slugify(scheme_name),
        "name": scheme_name,                                          # 1
        "description": parsed.get("description", ""),                 # 2
        "eligibility_criteria": parsed.get("eligibility_criteria", []),  # 3
        "benefits": parsed.get("benefits", []),                        # 4
        "required_documents": parsed.get("required_documents", []),   # 5
        "deadline": parsed.get("deadline"),                            # 6
        "restrictions_and_conditions": parsed.get("restrictions_and_conditions", []),  # 7
        "application_process": parsed.get("application_process", []), # 8
        "source_gr_pdf": source_document,                              # 9
        "rules": rules,                     # engine-only, not for display
        "active": False,
        "status": "pending_review",
        "requires_admin_review": True,
        "admin_notes": admin_notes,
    }

    from app.services.validate_schemes import validate_schemes
    validation_errors = validate_schemes([scheme])

    possible_duplicates = []
    if existing_scheme_names:
        possible_duplicates = find_possible_duplicate_schemes(scheme_name, existing_scheme_names)
        if possible_duplicates:
            scheme["admin_notes"].append(
                f"Possible duplicate: this scheme's name is similar to existing scheme(s) "
                f"{[m['existing_name'] for m in possible_duplicates]} — check whether this is "
                f"the same real-world scheme before approving, to avoid two live entries for "
                f"the same benefit."
            )

    return {
        "success": True,
        "scheme": scheme,
        "validation_errors": validation_errors,
        "possible_duplicates": possible_duplicates,
    }