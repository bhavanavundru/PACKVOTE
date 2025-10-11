from fastapi import APIRouter
from pydantic import BaseModel
from app.core.nlp_engine import NLPEngine

router = APIRouter(prefix="/api/chat", tags=["Chat"])

nlp_engine = NLPEngine()

class ChatRequest(BaseModel):
    user: str
    message: str

@router.post("/")
def process_message(data: ChatRequest):
    result = nlp_engine.extract_preferences(data.message)
    return {"user": data.user, "preferences": result}
