"""
scheme_service.py
====================

WHAT THIS FILE DOES:
  Stores extracted/admin-reviewed schemes and hands active ones to
  rule_engine.py. This is deliberately the SIMPLEST possible version —
  a JSON file on disk — not a real database. That's intentional:

  - It proves the admin-approval workflow end-to-end without anyone
    needing to set up PostgreSQL first.
  - Every function here (save_pending_scheme, approve_scheme,
    get_active_schemes, ...) has an obvious 1:1 mapping to a future
    database table row/query. Whoever builds the real DB layer later
    can keep these exact function names and just change what's inside
    them — nothing that CALLS this module needs to change.

STATUS LIFECYCLE OF A SCHEME:
    pending_review  -> just extracted, not yet checked by a human
    approved        -> admin reviewed it and it's live (active=True)
    rejected        -> admin reviewed it and declined it

HOW THIS CONNECTS TO rule_engine.py:
  rule_engine.py's check_eligibility() (and the other functions) already
  accept an optional `schemes=` parameter. So instead of:
      check_eligibility(profile)                       # uses hardcoded SCHEMES
  the FastAPI layer calls:
      check_eligibility(profile, schemes=get_active_schemes())
  rule_engine.py needed ZERO changes for this to work.
"""

import json
import os
from typing import Any, Dict, List, Optional

# Where scheme records live for now. A real database replaces this
# constant and the four functions below — nothing else changes.
STORAGE_PATH = os.path.join(os.path.dirname(__file__), "extracted_schemes.json")


def _load_all() -> List[Dict[str, Any]]:
    if not os.path.isfile(STORAGE_PATH):
        return []
    try:
        with open(STORAGE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as error:
        print(f"[scheme_service] WARNING: could not read {STORAGE_PATH}: {error}")
        return []


def _save_all(schemes: List[Dict[str, Any]]) -> None:
    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(schemes, f, indent=2, ensure_ascii=False)


def save_pending_scheme(scheme: Dict[str, Any]) -> Dict[str, Any]:
    """
    Saves a freshly-extracted scheme (from scheme_extractor.py) with
    status "pending_review". Does NOT check for duplicate scheme_id
    collisions here — that's exactly the kind of thing an admin reviewing
    the list should catch, not something to silently auto-resolve.
    """
    schemes = _load_all()
    schemes.append(scheme)
    _save_all(schemes)
    return scheme


def list_pending_schemes() -> List[Dict[str, Any]]:
    """Everything an admin still needs to review."""
    return [s for s in _load_all() if s.get("status") == "pending_review"]


def approve_scheme(scheme_id: str, approved_by: str = None) -> Optional[Dict[str, Any]]:
    """
    Marks a scheme approved and active. This is the ONLY function in the
    entire pipeline that is allowed to set "active": True — extraction
    never does this, on purpose.
    """
    schemes = _load_all()
    for scheme in schemes:
        if scheme.get("scheme_id") == scheme_id:
            scheme["status"] = "approved"
            scheme["active"] = True
            if approved_by:
                scheme["approved_by"] = approved_by
            _save_all(schemes)
            return scheme
    return None


def reject_scheme(scheme_id: str, reason: str = None) -> Optional[Dict[str, Any]]:
    """Marks a scheme rejected. It stays on record (for audit) but never
    becomes active."""
    schemes = _load_all()
    for scheme in schemes:
        if scheme.get("scheme_id") == scheme_id:
            scheme["status"] = "rejected"
            scheme["active"] = False
            if reason:
                scheme["rejection_reason"] = reason
            _save_all(schemes)
            return scheme
    return None


def get_active_schemes() -> List[Dict[str, Any]]:
    """
    The function rule_engine.py's `schemes=` parameter should be given.
    Only schemes an admin has approved come back — pending_review and
    rejected schemes are never included, so a not-yet-reviewed scheme
    can never accidentally affect a real eligibility check.
    """
    return [s for s in _load_all() if s.get("status") == "approved" and s.get("active")]