from app.services.gr_summarizer import extract_text_from_pdf
from app.services.scheme_extractor import extract_scheme
from app.services.scheme_service import save_pending_scheme

text = extract_text_from_pdf(
    "test_data/Scheme-BhausahebPhundkarFalbaagLagvadYojana.pdf"
)

print("PDF extracted:", len(text), "characters")

result = extract_scheme(text, summary_language="English")

if result["success"]:
    scheme = result["scheme"]

    saved = save_pending_scheme(scheme)

    print("Saved:", saved)
    print("Scheme ID:", scheme["scheme_id"])
    print("Status:", scheme["status"])
    print("Active:", scheme["active"])
else:
    print("Extraction failed")
    print(result)
