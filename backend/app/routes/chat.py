from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    user: str
    message: str

@router.post("/")
def process_message(data: ChatRequest):
    # Temporary response (will later call nlp_engine)
    print(f"Received message from {data.user}: {data.message}")
    return {
        "user": data.user,
        "message": data.message,
        "preferences": {"likes": ["beaches"], "dislikes": ["long hikes"]},
        "tone": "positive"
    }
