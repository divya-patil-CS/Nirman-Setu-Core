"""rule_engine.py

This module provides a generic evaluator that can check ANY rule against
ANY user profile, and functions built on top of it:

    check_eligibility(profile)                 -> basic scheme-level pass/fail
    check_component_eligibility(profile, id)   -> per-component pass/fail
                                                    (for schemes with sub-benefits)
    get_priority_factors(profile, id)          -> which priority factors match
                                                    (informational, never filters)
    calculate_remaining_eligible_area(profile, id) -> area math for schemes
                                                    where a previous benefit
                                                    reduces (not blocks) area

Scheme data itself (including "components", "priority_factors", and
"area_limits") lives in schemes_data.py — this file only contains logic.
"""

from typing import Any, Dict, List, Optional
import logging

from app.services.schemes_data import SCHEMES

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# FIELD LOOKUP (including the family_members virtual fields)
# ---------------------------------------------------------------------

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
            return relations

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


# ---------------------------------------------------------------------
# LEAF CONDITION EVALUATION
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
        logger.warning(
            f"Type mismatch comparing field '{field}' "
            f"(value={actual!r}) with expected={expected!r}: {e}"
        )
        return False


# ---------------------------------------------------------------------
# RULE (GROUP/LEAF) EVALUATION
# ---------------------------------------------------------------------

def evaluate_rule(profile: Dict[str, Any], rule: Dict[str, Any]) -> bool:
    """
    Evaluates a rule node, which is either:
      - a group: {"operator": "AND"/"OR", "conditions": [...]}
      - a leaf condition: {"field": ..., "op": ..., "value": ...}
    Recursive, so groups can nest to any depth.
    """
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
            logger.warning(f"Unsupported group operator '{operator}', defaulting to False")
            return False

    if "field" in rule and "op" in rule:
        return evaluate_condition(profile, rule)

    logger.warning(f"Unrecognized rule structure: {rule}")
    return False


# ---------------------------------------------------------------------
# SCHEME-LEVEL ELIGIBILITY (your original, unchanged behavior/shape)
# ---------------------------------------------------------------------

def check_eligibility(profile: Dict[str, Any], schemes: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """
    Given a user profile dict, checks it against every ACTIVE scheme's
    top-level "rules" and returns the list of schemes the user is
    eligible for, as {"scheme_id", "name", "deadline"} dicts.

    `schemes` defaults to the real SCHEMES list from schemes_data.py, but
    you can pass in your own list (e.g. dummy test schemes) to test the
    engine's LOGIC completely independently of real scheme data.

    NOTE: this only checks SCHEME-LEVEL eligibility. For schemes that also
    have "components" (like ambedkar_krushi_swavalamban) or
    "priority_factors" (like bhausaheb_fundkar_falbag), use the additional
    functions below to get that extra detail.
    """
    if schemes is None:
        schemes = SCHEMES

    if not profile or not isinstance(profile, dict):
        logger.warning("check_eligibility called with an invalid profile")
        return []

    eligible_schemes: List[Dict[str, Any]] = []

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
# HELPERS shared by the functions below
# ---------------------------------------------------------------------

def _find_scheme(scheme_id: str, schemes: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    if schemes is None:
        schemes = SCHEMES
    for scheme in schemes:
        if scheme.get("scheme_id") == scheme_id:
            return scheme
    return None


# ---------------------------------------------------------------------
# COMPONENT-LEVEL ELIGIBILITY
# ---------------------------------------------------------------------

def check_component_eligibility(
    profile: Dict[str, Any], scheme_id: str, schemes: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    For schemes with a "components" list (sub-benefits, each with their
    own minimum land requirement and amount), checks each component
    individually against the profile.

    A component is only checked at all if the profile passes the
    scheme-level "rules" first. If a component also has its own
    "eligibility_rule" (same AND/OR/condition shape as scheme-level
    "rules"), that is evaluated too using the same evaluate_rule()
    function — so component-specific conditions (e.g. "must not have
    already received a well benefit") are checked the same generic way
    as everything else, not as special-cased Python logic.

    Returns a list of dicts, one per component:
        {
            "component_id": "new_well",
            "name": "New Well",
            "amount_inr": 250000,
            "eligible": True/False,
            "requires_manual_review": True/False,
            "package_group": "well_or_pond_package" or None,
            "notes": "why not eligible, if applicable" or None,
        }

    "package_group" (when present) means this component is part of a set
    where the beneficiary may only choose ONE component from that group
    (e.g. new well OR old well repair OR farm pond lining, not more than
    one) — this is informational for your UI, not enforced here, since
    it's the applicant's own choice, not a pass/fail condition.
    """
    scheme = _find_scheme(scheme_id, schemes)
    if not scheme:
        logger.warning(f"check_component_eligibility: unknown scheme_id '{scheme_id}'")
        return []

    if not scheme.get("active", True):
        return []

    scheme_level_eligible = evaluate_rule(profile, scheme.get("rules", {}))

    results = []
    for component in scheme.get("components", []):
        notes = []
        component_eligible = False

        if not scheme_level_eligible:
            notes.append("Does not meet base scheme eligibility")
        else:
            min_land = component.get("min_land_hectares")
            actual_land = profile.get("agricultural_land_hectares")

            land_ok = True
            if min_land is not None:
                if actual_land is None:
                    land_ok = False
                    notes.append("agricultural_land_hectares not provided in profile")
                elif actual_land < min_land:
                    land_ok = False
                    notes.append(f"Needs at least {min_land} hectares for this component")

            extra_rule = component.get("eligibility_rule")
            extra_ok = True
            if extra_rule is not None:
                extra_ok = evaluate_rule(profile, extra_rule)
                if not extra_ok:
                    notes.append("Does not meet this component's specific conditions")

            component_eligible = land_ok and extra_ok

        requires_manual_review = component.get("previous_benefit_restriction") == "manual_review"

        results.append({
            "component_id": component.get("component_id"),
            "name": component.get("name"),
            "amount_inr": component.get("amount_inr"),
            "eligible": component_eligible,
            "requires_manual_review": requires_manual_review,
            "package_group": component.get("package_group"),
            "notes": "; ".join(notes) if notes else None,
        })

    return results


# ---------------------------------------------------------------------
# PRIORITY FACTORS (informational only — never disqualifies anyone)
# ---------------------------------------------------------------------

def get_priority_factors(
    profile: Dict[str, Any], scheme_id: str, schemes: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    For schemes with a "priority_factors" list, reports which ones the
    profile matches. These affect selection ORDER when a scheme has more
    applicants than funded slots — they never make someone ineligible.

    Returns a list of dicts:
        {"label": "SC/ST farmer priority", "matched": True/False}
    """
    scheme = _find_scheme(scheme_id, schemes)
    if not scheme:
        logger.warning(f"get_priority_factors: unknown scheme_id '{scheme_id}'")
        return []

    results = []
    for factor in scheme.get("priority_factors", []):
        matched = evaluate_condition(profile, factor)
        results.append({"label": factor.get("label"), "matched": matched})

    return results


# ---------------------------------------------------------------------
# REMAINING ELIGIBLE AREA (for schemes where a previous benefit shrinks,
# rather than blocks, how much area still qualifies)
# ---------------------------------------------------------------------

def calculate_remaining_eligible_area(
    profile: Dict[str, Any], scheme_id: str, schemes: Optional[List[Dict[str, Any]]] = None
) -> Optional[Dict[str, Any]]:
    """
    For schemes with "area_limits" defined (like bhausaheb_fundkar_falbag),
    works out how much area is still eligible after subtracting any
    previously-benefited area.

    Reads from the profile:
        "division"                       ("konkan" or anything else)
        "previous_benefit_area_hectares" (number, optional, defaults to 0)

    Returns None if this scheme has no "area_limits" defined. Otherwise
    returns:
        {
            "min_area_hectares": ...,
            "max_area_hectares": ...,
            "previously_used_hectares": ...,
            "remaining_eligible_hectares": ...,
        }
    """
    scheme = _find_scheme(scheme_id, schemes)
    if not scheme or "area_limits" not in scheme:
        return None

    division = (profile.get("division") or "other").lower()
    limits = scheme["area_limits"].get(division, scheme["area_limits"].get("other"))
    if not limits:
        return None

    max_area = limits["max"]
    used_area = profile.get("previous_benefit_area_hectares") or 0
    remaining_area = max(0, max_area - used_area)

    return {
        "min_area_hectares": limits["min"],
        "max_area_hectares": max_area,
        "previously_used_hectares": used_area,
        "remaining_eligible_hectares": remaining_area,
    }