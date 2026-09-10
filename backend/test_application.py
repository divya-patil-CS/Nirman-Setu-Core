from app.services.application_service import match_scheme_from_message

eligible = [{"scheme_id": "test_scheme", "name": "Test Scheme", "deadline": "2026-12-31"}]

result = match_scheme_from_message("I want to apply for Test Scheme", eligible)
print(result)

result2 = match_scheme_from_message("what is the weather today", eligible)
print(result2)