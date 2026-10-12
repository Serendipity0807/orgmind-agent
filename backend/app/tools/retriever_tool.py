"""工具:检索公司文档(RAG)"""
from langchain_core.tools import tool

from app.rag.retriever import get_retriever

retriever = get_retriever()

@tool
def search_company_docs(query: str) -> str:
    """
    检索公司内部文档(规章制度类:考勤、请假、报销、加班等)。

    当用户问题涉及公司制度、流程、规定时,使用本工具。
    入参 query:用自然语言描述要检索的内容,例如"差旅报销住宿费标准"。
    """

    docs = retriever.invoke(query)
    if not docs:
        return "没有检索到相关文档内容"

    return "\n\n".join(
        f"[来源:{doc.metadata.get('source', '未知')}]\n{doc.page_content}"
        for doc in docs
    )