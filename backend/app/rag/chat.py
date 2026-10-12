from langchain_core.messages import SystemMessage,HumanMessage
from langchain_openai import ChatOpenAI

from app.rag.retriever import get_retriever
from app.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

llm = ChatOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    model=DEEPSEEK_MODEL,
)

retriever = get_retriever()

SYSTEM_PROMPT = (
    "你是公司的知识助手。请只依据下面提供的资料回答问题。"
    "如果资料中没有答案,请直接说“根据现有资料无法回答”,不要编造。"
    "回答要简洁、准确。"
)

def answer(question:str):
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    messages = [
        SystemMessage(content = SYSTEM_PROMPT),
        HumanMessage(content = f"[资料]:\n{context}\n\n[问题]:\n{question}"),
    ]
    return llm.invoke(messages).content