"""
validate_schemes.py
======================

Run this any time you add or edit a scheme in SCHEMES, to catch mistakes
BEFORE they cause a scheme to silently match every user (or no user).

HOW TO RUN:
    cd backend
    python -m app.services.validate_schemes

WHAT IT CHECKS (per scheme):
    - scheme_id, name are present and scheme_id is unique across all schemes
    - "rules" exists and is not empty/missing (empty rules = matches everyone,
      per evaluate_rule's design — almost never what you actually want)
    - every leaf condition has "field", "op", and "value"
    - "op" is one of the operators evaluate_condition actually supports
    - every group has "operator" set to "AND" or "OR"

This does NOT check whether the LOGIC is correct (e.g. whether the income
cutoff is the right number) — only whether the STRUCTURE is well-formed.
"""

from app.services.rule_engine import SCHEMES

VALID_OPS = {"==", "!=", "<", "<=", ">", ">=", "in", "not_in"}
VALID_GROUP_OPERATORS = {"AND", "OR"}


def validate_rule_node(node: dict, scheme_id: str, errors: list) -> None:
    """Recursively checks one rule node (group or leaf) for structural problems."""
    if not isinstance(node, dict):
        errors.append(f"[{scheme_id}] rule node is not a dict: {node!r}")
        return

    is_group = "operator" in node and "conditions" in node
    is_leaf = "field" in node and "op" in node

    if is_group:
        if node["operator"].upper() not in VALID_GROUP_OPERATORS:
            errors.append(f"[{scheme_id}] invalid group operator: {node['operator']!r}")
        if not node["conditions"]:
            errors.append(f"[{scheme_id}] group has an empty 'conditions' list")
        for sub_node in node.get("conditions", []):
            validate_rule_node(sub_node, scheme_id, errors)

    elif is_leaf:
        if node["op"] not in VALID_OPS:
            errors.append(f"[{scheme_id}] invalid operator '{node['op']}' (field: {node.get('field')})")
        if "value" not in node:
            errors.append(f"[{scheme_id}] condition on field '{node.get('field')}' is missing 'value'")

    else:
        errors.append(f"[{scheme_id}] rule node doesn't look like a group or a leaf: {node}")


def validate_schemes(schemes: list = None) -> list:
    """
    Returns a list of human-readable error strings. Empty list = all good.

    `schemes` defaults to the real SCHEMES from rule_engine.py, but you
    can pass in a single freshly-extracted scheme (as a one-item list) to
    validate it BEFORE it's added to SCHEMES at all — this is exactly
    what scheme_extractor.py does after Gemini produces a new scheme.
    """
    if schemes is None:
        schemes = SCHEMES

    errors = []
    seen_ids = set()

    for scheme in schemes:
        scheme_id = scheme.get("scheme_id")

        if not scheme_id:
            errors.append("A scheme is missing 'scheme_id' entirely")
            continue
        if scheme_id in seen_ids:
            errors.append(f"Duplicate scheme_id: '{scheme_id}'")
        seen_ids.add(scheme_id)

        if not scheme.get("name"):
            errors.append(f"[{scheme_id}] missing 'name'")

        rules = scheme.get("rules")
        if not rules:
            errors.append(
                f"[{scheme_id}] 'rules' is missing or empty — this scheme will match EVERY user!"
            )
            continue

        validate_rule_node(rules, scheme_id, errors)

    return errors


if __name__ == "__main__":
    problems = validate_schemes()
    if not problems:
        print(f"[PASS] All {len(SCHEMES)} schemes in schemes_data.py are structurally valid.")
    else:
        print(f"[FAIL] Found {len(problems)} problem(s):\n")
        for problem in problems:
            print(f"  - {problem}")