"""
rule_engine.py

This module stores government scheme eligibility rules as structured
data (dicts/JSON) instead of hardcoded if/else logic, and provides a
generic evaluator that can check ANY rule against ANY user profile.

Why this design?
- To add a new scheme, you just add a new dict to SCHEMES below.
- You never need to touch the evaluation code again.
"""

from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# 1. SCHEME DATA
# ---------------------------------------------------------------------
# In a real system this would live in the PostgreSQL database (a table
# of schemes with a JSON column for "rules"). For now, to keep things
# simple while you build and test, we store it as a Python list of
# dicts right here. Later, swapping this for a DB read is a small change
# because the rest of the code doesn't care where the data comes from.

SCHEMES: List[Dict[str, Any]] = [
    {
        "scheme_id": "farmer_income_scheme",
        "name": "Farmer Income Support Scheme",
        "deadline": "2026-12-31",
        "active": True,
        "rules": {
            "operator": "AND",
            "conditions": [
                {"field": "occupation", "op": "==", "value": "farmer"},
                {"field": "annual_income", "op": "<=", "value": 250000},
            ],
        },
    },
    {
        "scheme_id": "senior_citizen_pension",
        "name": "Senior Citizen Pension Scheme",
        "deadline": "2026-10-15",
        "active": True,
        "rules": {
            "operator": "AND",
            "conditions": [
                {"field": "age", "op": ">=", "value": 60},
                {"field": "annual_income", "op": "<=", "value": 300000},
            ],
        },
    },
    {
        # Example showing nested groups: (occupation == farmer OR occupation == laborer)
        # AND income <= 200000
        "scheme_id": "rural_worker_scheme",
        "name": "Rural Worker Support Scheme",
        "deadline": "2026-11-30",
        "active": True,
        "rules": {
            "operator": "AND",
            "conditions": [
                {
                    "operator": "OR",
                    "conditions": [
                        {"field": "occupation", "op": "==", "value": "farmer"},
                        {"field": "occupation", "op": "==", "value": "laborer"},
                    ],
                },
                {"field": "annual_income", "op": "<=", "value": 200000},
            ],
        },
    },
]


# ---------------------------------------------------------------------
# 2. GETTING A VALUE OUT OF THE PROFILE
# ---------------------------------------------------------------------
# Most fields (age, occupation, annual_income, gender, caste) are just
# plain keys in the profile dict, so we can look them up directly.
#
# But "family_members" is a LIST of {relation, age} dicts, so a rule
# can't just say profile["family_members"] <= 5. Instead, we support a
# few special "virtual fields" using dot notation:
#
#   "family_members.count"            -> how many family members
#   "family_members.has_relation"     -> True/False, used with op "==" and
#                                         value being the relation name,
#                                         e.g. {"field": "family_members.has_relation",
#                                               "op": "==", "value": "mother"}
#   "family_members.min_age"          -> youngest family member's age
#   "family_members.max_age"          -> oldest family member's age
#
# If you need more later, add another "elif" here — you won't need to
# touch anything else.

def get_field_value(profile: Dict[str, Any], field: str) -> Any:
    """
    Pulls a value out of the profile dict for a given field name.
    Returns None if the field doesn't exist or can't be computed,
    so that comparisons fail safely instead of crashing.
    """
    try:
        if field == "family_members.count":
            return len(profile.get("family_members") or [])

        if field == "family_members.has_relation":
            members = profile.get("family_members") or []
            relations = {m.get("relation", "").lower() for m in members}
            return relations  # caller compares membership; see evaluate_condition

        if field == "family_members.min_age":
            members = profile.get("family_members") or []
            ages = [m.get("age") for m in members if m.get("age") is not None]
            return min(ages) if ages else None

        if field == "family_members.max_age":
            members = profile.get("family_members") or []
            ages = [m.get("age") for m in members if m.get("age") is not None]
            return max(ages) if ages else None

        # Default case: plain top-level field like "age", "occupation", etc.
        return profile.get(field)

    except Exception as e:
        # If anything goes wrong reading this field, log it and return
        # None rather than crashing the whole eligibility check.
        logger.warning(f"Could not read field '{field}' from profile: {e}")
        return None


# ---------------------------------------------------------------------
# 3. EVALUATING A SINGLE LEAF CONDITION
# ---------------------------------------------------------------------

def evaluate_condition(profile: Dict[str, Any], condition: Dict[str, Any]) -> bool:
    """
    Evaluates one leaf condition, e.g.
        {"field": "annual_income", "op": "<=", "value": 250000}
    against the profile. Returns True or False.
    """
    field = condition.get("field")
    op = condition.get("op")
    expected = condition.get("value")

    actual = get_field_value(profile, field)

    # Special case: "has_relation" gives us back a SET of relations,
    # so "==" / "!=" here really mean "is in the set" / "is not in the set".
    if field == "family_members.has_relation":
        if actual is None:
            return False
        expected_lower = str(expected).lower()
        if op == "==":
            return expected_lower in actual
        if op == "!=":
            return expected_lower not in actual
        logger.warning(f"Unsupported op '{op}' for family_members.has_relation")
        return False

    # If the profile simply doesn't have this field, treat as not eligible
    # rather than crashing.
    if actual is None:
        return False

    try:
        if op == "==":
            return actual == expected
        elif op == "!=":
            return actual != expected
        elif op == "<":
            return actual < expected
        elif op == "<=":
            return actual <= expected
        elif op == ">":
            return actual > expected
        elif op == ">=":
            return actual >= expected
        elif op == "in":
            return actual in expected
        elif op == "not_in":
            return actual not in expected
        else:
            logger.warning(f"Unsupported operator '{op}' in rule condition")
            return False
    except TypeError as e:
        # Happens e.g. if you try to compare a string to a number.
        # We treat this as "condition not met" instead of crashing.
        logger.warning(
            f"Type mismatch comparing field '{field}' "
            f"(value={actual!r}) with expected={expected!r}: {e}"
        )
        return False


# ---------------------------------------------------------------------
# 4. EVALUATING A RULE (which may contain nested groups)
# ---------------------------------------------------------------------

def evaluate_rule(profile: Dict[str, Any], rule: Dict[str, Any]) -> bool:
    """
    Evaluates a rule node, which is either:
      - a group: {"operator": "AND"/"OR", "conditions": [...]}
        where each item in "conditions" is itself a rule node
        (leaf condition OR another nested group)
      - a leaf condition: {"field": ..., "op": ..., "value": ...}

    This function calls itself recursively for nested groups, which is
    how we support things like (A OR B) AND C without limit on depth.
    """
    if not rule:
        # An empty/missing rule means "no restriction" -> eligible.
        return True

    # A "group" node has "operator" and "conditions".
    if "operator" in rule and "conditions" in rule:
        operator = rule["operator"].upper()
        sub_results = [evaluate_rule(profile, sub_rule) for sub_rule in rule["conditions"]]

        if operator == "AND":
            return all(sub_results)
        elif operator == "OR":
            return any(sub_results)
        else:
            logger.warning(f"Unsupported group operator '{operator}', defaulting to False")
            return False

    # A "leaf" node has "field", "op", "value".
    if "field" in rule and "op" in rule:
        return evaluate_condition(profile, rule)

    # If we don't recognize the shape of this rule node, log it and
    # fail safe (treat as not matching) instead of crashing.
    logger.warning(f"Unrecognized rule structure: {rule}")
    return False


# ---------------------------------------------------------------------
# 5. (Preview only — we'll build this properly in the next step)
# ---------------------------------------------------------------------
# def check_eligibility(profile: dict) -> list[dict]:
#     ...loops through SCHEMES, calls evaluate_rule for each, collects matches...
# ---------------------------------------------------------------------
# 5. MAIN FUNCTION: CHECK ELIGIBILITY FOR ALL SCHEMES
# ---------------------------------------------------------------------

def check_eligibility(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Given a user profile dict (as produced by the chatbot), checks it
    against every ACTIVE scheme in SCHEMES and returns a list of the
    schemes the user is eligible for.

    Each item in the returned list looks like:
        {"scheme_id": "...", "name": "...", "deadline": "..."}

    If profile is missing, empty, or badly formed, this returns an
    empty list instead of crashing — so the calling code (e.g. an API
    route) can safely show "no eligible schemes found" rather than
    erroring out.
    """
    if not profile or not isinstance(profile, dict):
        logger.warning("check_eligibility called with an invalid profile")
        return []

    eligible_schemes: List[Dict[str, Any]] = []

    for scheme in SCHEMES:
        # Skip schemes that have been turned off (e.g. deadline passed,
        # or an admin disabled it) without deleting their data.
        if not scheme.get("active", True):
            continue

        try:
            is_eligible = evaluate_rule(profile, scheme.get("rules", {}))
        except Exception as e:
            # Extra safety net: if one scheme's rule is malformed, log
            # it and skip that scheme, rather than crashing the whole
            # eligibility check for every other scheme too.
            logger.error(f"Error evaluating scheme '{scheme.get('scheme_id')}': {e}")
            continue

        if is_eligible:
            eligible_schemes.append({
                "scheme_id": scheme.get("scheme_id"),
                "name": scheme.get("name"),
                "deadline": scheme.get("deadline"),
            })

    return eligible_schemes