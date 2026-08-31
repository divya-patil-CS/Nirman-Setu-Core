from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chatbot_service import chat_step
from app.services.rule_engine import check_eligibility

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    profile: dict = {}
    history: list = []
    language: str = "Hindi"

@router.post("/chat")
def chat(request: ChatRequest):
    result = chat_step(request.message, request.profile, request.history, request.language)
    if result["profile_complete"]:
        result["eligible_schemes"] = check_eligibility(result["profile"])
    return result