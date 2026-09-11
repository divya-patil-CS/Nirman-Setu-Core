"""
test_gr_summarizer_manually.py
=================================

Run this to test gr_summarizer.py — both the text-based path and the
new PDF-upload path.

HOW TO RUN (from your terminal):
    cd backend
    python3 -m app.services.test_gr_summarizer_manually

WHAT TO EXPECT:
  Part 1 tests error handling and does NOT need internet or an API key —
  it should always show [PASS].

  Part 2 makes a REAL call to Gemini using plain text (needs
  GEMINI_API_KEY in your .env and internet).

  Part 3 makes REAL calls to Gemini using actual PDF files (needs the
  same, PLUS the two PDF files to actually exist at the paths below —
  update PDF_PATH_1 / PDF_PATH_2 to wherever you saved them).

  Parts 2 and 3 don't have a strict [PASS]/[FAIL] — AI output isn't
  identical every run. Read the printed summary yourself and judge
  whether it makes sense (covers benefit, eligibility, documents, and is
  in the right language).
"""

import os
from app.services.gr_summarizer import summarize_gr, summarize_gr_from_pdf, GEMINI_API_KEY


SAMPLE_GR_TEXT = """
GOVERNMENT RESOLUTION
Subject: Scheme for Financial Assistance to Small and Marginal Farmers

1. The State Government hereby sanctions a scheme under which eligible
   farmers shall receive a direct benefit transfer of Rs. 6,000 per year,
   paid in three equal installments of Rs. 2,000 each, credited directly to
   the farmer's bank account.

2. Eligibility: The applicant must (a) own cultivable agricultural land not
   exceeding 2 hectares, (b) have an annual family income not exceeding
   Rs. 2,50,000, and (c) not be a government employee or income-tax payee.

3. Documents required at the time of application: (a) Aadhaar Card,
   (b) 7/12 land record extract or equivalent land ownership document,
   (c) active bank account passbook copy, (d) recent passport-size
   photograph.

4. Applications shall be submitted through the online portal or at the
   nearest Common Service Centre (CSC).
"""

# EDIT THESE two paths to point at wherever you saved the two real GR
# PDFs on your machine (e.g. inside a backend/test_data/ folder you
# create and put the files in).
PDF_PATH_1 = "test_data/Scheme-DrBabasahebAmbedkarKrushiSwavalambanYojana.pdf"
PDF_PATH_2 = "test_data/Scheme-BhausahebPhundkarFalbaagLagvadYojana.pdf"


def check(label: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}")


if __name__ == "__main__":
    print("--- Part 1: error handling (no API needed) ---")

    result = summarize_gr(gr_text="", language="Hindi")
    check("Empty GR text should fail cleanly", result["success"] is False)

    result = summarize_gr(gr_text="Some text", language="")
    check("Empty language should fail cleanly", result["success"] is False)

    result = summarize_gr(gr_text="   ", language="Hindi")
    check("Whitespace-only GR text should fail cleanly", result["success"] is False)

    result = summarize_gr_from_pdf(pdf_path="/nonexistent/file.pdf", language="Marathi")
    check("Missing PDF file should fail cleanly", result["success"] is False)

    print("\n--- Part 2: real Gemini API call (plain text) ---")
    if not GEMINI_API_KEY:
        print(
            "[SKIPPED] GEMINI_API_KEY is not set, so I can't make a real API call.\n"
            "          Add it to a .env file in your backend/ folder to run this part:\n"
            "              GEMINI_API_KEY=your_actual_key_here"
        )
    else:
        result = summarize_gr(
            gr_text=SAMPLE_GR_TEXT,
            language="Hindi",
            scheme_name="Financial Assistance to Small and Marginal Farmers",
        )
        if result["success"]:
            print("[INFO] Got a summary back. Read it and judge if it makes sense:\n")
            print(result["summary"])
        else:
            print(f"[FAIL] The API call failed: {result['error']}")

    print("\n--- Part 3: real Gemini API calls using actual PDF files ---")
    if not GEMINI_API_KEY:
        print("[SKIPPED] GEMINI_API_KEY is not set (see Part 2 above).")
    else:
        for label, path in [
            ("Ambedkar Krushi Swavalamban Yojana (garbled-font PDF)", PDF_PATH_1),
            ("Bhausaheb Fundkar Falbag Lagvad Yojana (clean-text PDF)", PDF_PATH_2),
        ]:
            print(f"\n[{label}]")
            if not os.path.isfile(path):
                print(f"[SKIPPED] File not found at '{path}'. Update PDF_PATH_1/PDF_PATH_2 "
                      f"at the top of this file to the real location on your machine.")
                continue

            result = summarize_gr_from_pdf(pdf_path=path, language="Marathi", scheme_name=label)
            if result["success"]:
                print("[INFO] Got a summary back. Read it and judge if it makes sense:\n")
                print(result["summary"])
            else:
                print(f"[FAIL] The API call failed: {result['error']}")

    print("\nDone.")