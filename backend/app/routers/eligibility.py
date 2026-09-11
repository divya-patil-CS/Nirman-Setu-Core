from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.services.scheme_service import get_active_schemes
from app.services.schemes_data import SCHEMES  # <-- the fix: also include hand-written schemes
from app.services.rule_engine import check_eligibility_detailed

router = APIRouter(
    prefix="/eligibility",
    tags=["Eligibility"]
)


class FarmerProfile(BaseModel):
    occupation: Optional[str] = None
    annual_income: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    caste: Optional[str] = None
    beneficiary_type: Optional[str] = None
    division: Optional[str] = None
    agricultural_land_hectares: Optional[float] = None
    aadhaar_available: Optional[bool] = None
    bank_account_linked_aadhaar: Optional[bool] = None
    farm_category: Optional[str] = None
    has_disability: Optional[bool] = None
    family_livelihood_only_agriculture: Optional[bool] = None
    family_members: Optional[List[Dict[str, Any]]] = None


@router.post("/check")
def check_farmer_eligibility(profile: FarmerProfile):
    farmer_profile = profile.model_dump(exclude_none=True)

    # Combine both sources: schemes you've hand-written in schemes_data.py,
    # PLUS anything an admin has approved through the AI-extraction
    # pipeline (scheme_service.py). Using only one or the other means
    # real, working schemes silently never get checked.
    active_schemes = SCHEMES + get_active_schemes()

    results = check_eligibility_detailed(
        farmer_profile,
        schemes=active_schemes
    )
    return {
        "success": True,
        "results": results
    }