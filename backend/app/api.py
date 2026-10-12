from fastapi import APIRouter
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

from app.config import DEEPSEEK_API_KEY ,DEEPSEEK_BASE_URL,DEEPSEEK_MODEL

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

llm = ChatOpenAI(
    model = DEEPSEEK_MODEL,
    base_url = DEEPSEEK_BASE_URL,
    api_key = DEEPSEEK_API_KEY,
)

@router.post("/api/chat")
def chat(req: ChatRequest):
    reply = llm.invoke(req.message)
    return {"reply": reply.content}