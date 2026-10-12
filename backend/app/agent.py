"""Agent 组装:让大模型自己决定查文档还是查数据库"""
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from app.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL
from app.tools.retriever_tool import search_company_docs
from app.tools.sql_tool import query_org_db

llm = ChatOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    model=DEEPSEEK_MODEL,
)

SYSTEM_PROMPT = (
    "你是 OrgMind,公司的知识助手。你可以使用工具查询公司文档和组织数据库,"
    "然后基于工具返回的结果回答用户问题。"
    "如果工具没有查到答案,就诚实地说不知道,不要编造。回答要简洁、准确。"
)

tools = [search_company_docs, query_org_db]

agent = create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)


def answer(question: str) -> str:
    """Agent 主入口:自动判断用哪个工具,返回最终答案"""
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content
