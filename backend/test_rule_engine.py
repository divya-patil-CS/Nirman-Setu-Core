from app.services.rule_engine import check_eligibility

# A farmer with low income — should match farmer_income_scheme and rural_worker_scheme
profile1 = {
    "name": "Ramesh",
    "age": 45,
    "occupation": "farmer",
    "annual_income": 180000,
    "family_members": [{"relation": "daughter", "age": 15}]
}
print("Profile 1 (farmer, low income):")
print(check_eligibility(profile1))
print()

# A senior citizen — should match senior_citizen_pension only
profile2 = {
    "name": "Sunita",
    "age": 65,
    "occupation": "retired",
    "annual_income": 150000
}
print("Profile 2 (senior citizen):")
print(check_eligibility(profile2))
print()

# Someone who matches nothing
profile3 = {
    "name": "Amit",
    "age": 30,
    "occupation": "software engineer",
    "annual_income": 900000
}
print("Profile 3 (no matches expected):")
print(check_eligibility(profile3))
print()

# Edge case: empty/invalid profile — should not crash
print("Empty profile:")
print(check_eligibility({}))