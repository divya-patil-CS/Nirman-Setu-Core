"""
rule_engine.py

This module provides a generic evaluator that can check ANY rule against
ANY user profile, and functions built on top of it.
"""

from typing import Any, Dict, List, Optional
import logging

from app.services.schemes_data import SCHEMES

logger = logging.getLogger(__name__)


def get_field_value(profile: Dict[str, Any], field: str) -> Any:
    try:
        if field == "family_members.count":
            return len(profile.get("family_members") or [])
        if field == "family_members.has_relation":
            members = profile.get("family_members") or []
            return {m.get("relation", "").lower() for m in members}
        if field == "family_members.min_age":
            members = profile.get("family_members") or []
            ages = [m.get("age") for m in members if m.get("age") is not None]
            return min(ages) if ages else None
        if field == "family_members.max_age":
            members = profile.get("family_members") or []
            ages = [m.get("age") for m in members if m.get("age") is not None]
            return max(ages) if ages else None
        return profile.get(field)
    except Exception as e:
        logger.warning(f"Could not read field '{field}' from profile: {e}")
        return None


def evaluate_condition(profile: Dict[str, Any], condition: Dict[str, Any]) -> bool:
    field = condition.get("field")
    op = condition.get("op")
    expected = condition.get("value")
    actual = get_field_value(profile, field)

    if field == "family_members.has_relation":
        if actual is None:
            return False
        expected_lower = str(expected).lower()
        if op == "==":
            return expected_lower in actual
        if op == "!=":
            return expected_lower not in actual
        return False

    if actual is None:
        return False

    try:
        if op == "==": return actual == expected
        elif op == "!=": return actual != expected
        elif op == "<": return actual < expected
        elif op == "<=": return actual <= expected
        elif op == ">": return actual > expected
        elif op == ">=": return actual >= expected
        elif op == "in": return actual in expected
        elif op == "not_in": return actual not in expected
        else:
            logger.warning(f"Unsupported operator '{op}'")
            return False
    except TypeError as e:
        logger.warning(f"Type mismatch: {e}")
        return False


def evaluate_rule(profile: Dict[str, Any], rule: Dict[str, Any]) -> bool:
    if not rule:
        return True
    if "operator" in rule and "conditions" in rule:
        operator = rule["operator"].upper()
        sub_results = [evaluate_rule(profile, sub_rule) for sub_rule in rule["conditions"]]
        if operator == "AND":
            return all(sub_results)
        elif operator == "OR":
            return any(sub_results)
        else:
            return False
    if "field" in rule and "op" in rule:
        return evaluate_condition(profile, rule)
    return False


def check_eligibility(profile: Dict[str, Any], schemes: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    if schemes is None:
        schemes = SCHEMES
    if not profile or not isinstance(profile, dict):
        return []
    eligible_schemes = []
    for scheme in schemes:
        if not scheme.get("active", True):
            continue
        try:
            is_eligible = evaluate_rule(profile, scheme.get("rules", {}))
        except Exception as e:
            logger.error(f"Error evaluating scheme '{scheme.get('scheme_id')}': {e}")
            continue
        if is_eligible:
            eligible_schemes.append({
                "scheme_id": scheme.get("scheme_id"),
                "name": scheme.get("name"),
                "deadline": scheme.get("deadline"),
            })
    return eligible_schemes


# ---------------------------------------------------------------------
# EXPLAINABLE ELIGIBILITY
# ---------------------------------------------------------------------
# check_eligibility() above answers one question: "which schemes does
# this profile qualify for?" — and a user who qualifies for nothing gets
# back an empty list, with no way to tell "you're not eligible" apart
# from "we don't know yet, some information is missing."
#
# check_eligibility_detailed() below answers three questions per scheme:
#   - Does the profile definitely qualify?      -> ELIGIBLE
#   - Does the profile definitely NOT qualify?  -> NOT_ELIGIBLE
#   - Can't tell — some needed field is missing? -> NEEDS_VERIFICATION
# and explains exactly which individual conditions passed, which failed,
# and which couldn't be checked because a profile field was missing.
#
# This uses three-valued logic (PASS / FAIL / MISSING) instead of plain
# True/False for each condition, because "the profile doesn't have this
# field" and "the profile has this field and it fails the check" are
# different situations that deserve different eligibility statuses.

_OPERATOR_PHRASES = {
    "==": "must be",
    "!=": "must not be",
    "<": "must be less than",
    "<=": "must be at most",
    ">": "must be more than",
    ">=": "must be at least",
    "in": "must be one of",
    "not_in": "must not be one of",
}


def _describe_condition(condition: Dict[str, Any], actual_value: Any, result: str) -> str:
    """Builds a human-readable explanation for one leaf condition."""
    field = condition.get("field")
    op = condition.get("op")
    expected = condition.get("value")
    phrase = _OPERATOR_PHRASES.get(op, op)

    if field == "family_members.has_relation":
        relation_phrase = "must include" if op == "==" else "must not include"
        return f"Family members {relation_phrase} a relative described as '{expected}'"

    base = f"{field} {phrase} {expected!r}"
    if result == "MISSING":
        return f"{base} (this information was not provided)"
    return f"{base} (your value: {actual_value!r})"


def evaluate_condition_detailed(profile: Dict[str, Any], condition: Dict[str, Any]) -> Dict[str, Any]:
    """
    Same checks as evaluate_condition(), but returns "PASS"/"FAIL"/
    "MISSING" instead of True/False, plus a human-readable description.
    """
    field = condition.get("field")
    op = condition.get("op")
    expected = condition.get("value")
    actual = get_field_value(profile, field)

    if field == "family_members.has_relation":
        if actual is None:
            result = "MISSING"
        else:
            expected_lower = str(expected).lower()
            matched = expected_lower in actual if op == "==" else expected_lower not in actual
            result = "PASS" if matched else "FAIL"
        return {"description": _describe_condition(condition, actual, result), "result": result}

    if actual is None:
        result = "MISSING"
    else:
        try:
            if op == "==": passed = actual == expected
            elif op == "!=": passed = actual != expected
            elif op == "<": passed = actual < expected
            elif op == "<=": passed = actual <= expected
            elif op == ">": passed = actual > expected
            elif op == ">=": passed = actual >= expected
            elif op == "in": passed = actual in expected
            elif op == "not_in": passed = actual not in expected
            else:
                passed = False
            result = "PASS" if passed else "FAIL"
        except TypeError:
            result = "FAIL"

    return {"description": _describe_condition(condition, actual, result), "result": result}


def evaluate_rule_detailed(profile: Dict[str, Any], rule: Dict[str, Any], collected: list = None) -> str:
    """
    Same tree-walk as evaluate_rule(), but using three-valued logic:
        AND: FAIL if any child FAILs; else MISSING if any child is
             MISSING; else PASS.
        OR:  PASS if any child PASSes; else MISSING if any child is
             MISSING; else FAIL.
    Every LEAF condition's individual result gets appended to `collected`
    (a list the caller passes in) regardless of the overall group
    result — this is what lets check_eligibility_detailed() report
    "these specific conditions passed / failed / are missing" rather
    than just a single yes/no for the whole scheme.
    """
    if collected is None:
        collected = []

    if not rule:
        return "PASS"

    if "operator" in rule and "conditions" in rule:
        operator = rule["operator"].upper()
        child_results = [evaluate_rule_detailed(profile, sub_rule, collected) for sub_rule in rule["conditions"]]

        if operator == "AND":
            if "FAIL" in child_results:
                return "FAIL"
            if "MISSING" in child_results:
                return "MISSING"
            return "PASS"
        elif operator == "OR":
            if "PASS" in child_results:
                return "PASS"
            if "MISSING" in child_results:
                return "MISSING"
            return "FAIL"
        else:
            return "FAIL"

    if "field" in rule and "op" in rule:
        leaf_result = evaluate_condition_detailed(profile, rule)
        collected.append(leaf_result)
        return leaf_result["result"]

    return "FAIL"


_STATUS_MAP = {"PASS": "ELIGIBLE", "FAIL": "NOT_ELIGIBLE", "MISSING": "NEEDS_VERIFICATION"}


def check_eligibility_detailed(profile: Dict[str, Any], schemes: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """
    THE FUNCTION eligibility.py (your router) SHOULD CALL.

    Unlike check_eligibility(), this returns ONE ENTRY PER ACTIVE SCHEME
    — never an empty list just because nobody matched — each with an
    explicit status and a full explanation:

        {
            "scheme_id": "...",
            "name": "...",
            "deadline": "...",
            "status": "ELIGIBLE" | "NOT_ELIGIBLE" | "NEEDS_VERIFICATION",
            "reasons": {
                "passed_criteria": ["..."],
                "failed_criteria": ["..."],
                "missing_information": ["..."],
            },
        }

    NEEDS_VERIFICATION means: nothing failed outright, but at least one
    condition couldn't be checked because the profile is missing a
    field the rule needs — this is different from NOT_ELIGIBLE and
    should be shown differently in the frontend (e.g. "we need more
    information" rather than "you don't qualify").
    """
    if schemes is None:
        schemes = SCHEMES
    if not profile or not isinstance(profile, dict):
        return []

    results = []
    for scheme in schemes:
        if not scheme.get("active", True):
            continue

        collected = []
        try:
            overall_result = evaluate_rule_detailed(profile, scheme.get("rules", {}), collected)
        except Exception as e:
            logger.error(f"Error evaluating scheme '{scheme.get('scheme_id')}': {e}")
            continue

        results.append({
            "scheme_id": scheme.get("scheme_id"),
            "name": scheme.get("name"),
            "deadline": scheme.get("deadline"),
            "status": _STATUS_MAP.get(overall_result, "NOT_ELIGIBLE"),
            "reasons": {
                "passed_criteria": [c["description"] for c in collected if c["result"] == "PASS"],
                "failed_criteria": [c["description"] for c in collected if c["result"] == "FAIL"],
                "missing_information": [c["description"] for c in collected if c["result"] == "MISSING"],
            },
        })

    return results