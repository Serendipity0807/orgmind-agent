from fastapi import APIRouter
from pydantic import BaseModel

from app.agent import answer

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/api/chat")
def chat(req: ChatRequest):
    return {"reply": answer(req.message)}