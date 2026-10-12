from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.chat import answer

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/api/chat")
def chat(req: ChatRequest):
    return {"reply": answer(req.message)}