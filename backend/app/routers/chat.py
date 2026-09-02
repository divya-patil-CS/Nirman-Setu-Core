from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chatbot_service import chat_step
from app.services.rule_engine import check_eligibility
from app.services.application_service import match_scheme_from_message, is_confirmation, is_rejection

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    profile: dict = {}
    history: list = []
    language: str = "Hindi"
    eligible_schemes: list = []
    selected_scheme: dict = None

@router.post("/chat")
def chat(request: ChatRequest):
    # STAGE 3: A scheme was already selected, waiting for yes/no confirmation
    if request.selected_scheme:
        if is_confirmation(request.message):
            return {
                "reply": f"Your application for {request.selected_scheme['name']} has been submitted successfully!",
                "profile": request.profile,
                "profile_complete": True,
                "history": request.history,
                "eligible_schemes": request.eligible_schemes,
                "selected_scheme": request.selected_scheme,
                "application_status": "submitted"
            }
        elif is_rejection(request.message):
            return {
                "reply": "No problem, we haven't submitted it. Let me know if you'd like to apply for a different scheme.",
                "profile": request.profile,
                "profile_complete": True,
                "history": request.history,
                "eligible_schemes": request.eligible_schemes,
                "selected_scheme": None,
                "application_status": "cancelled"
            }
        else:
            return {
                "reply": f"Just to confirm — should I submit your application for {request.selected_scheme['name']}? Please say yes or no.",
                "profile": request.profile,
                "profile_complete": True,
                "history": request.history,
                "eligible_schemes": request.eligible_schemes,
                "selected_scheme": request.selected_scheme,
                "application_status": "awaiting_confirmation"
            }

    # STAGE 2: Eligible schemes already shown, check if user is picking one
    if request.eligible_schemes:
        matched = match_scheme_from_message(request.message, request.eligible_schemes)
        if matched:
            return {
                "reply": f"Great! Let's proceed with your application for {matched['name']}. "
                         f"The deadline is {matched['deadline']}. Shall I go ahead and submit it?",
                "profile": request.profile,
                "profile_complete": True,
                "history": request.history,
                "eligible_schemes": request.eligible_schemes,
                "selected_scheme": matched,
                "application_status": "awaiting_confirmation"
            }

    # STAGE 1: Normal onboarding/profile-building flow
    result = chat_step(request.message, request.profile, request.history, request.language)

    if result["profile_complete"]:
        result["eligible_schemes"] = check_eligibility(result["profile"])

    return result