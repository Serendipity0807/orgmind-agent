from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app.config import EMBEDDING_MODEL,CHROMA_DIR

def get_retriever(k = 3):
    """加载向量化模型,返回检索器"""
    embeddings = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL)
    vectorstore = Chroma(
        embedding_function = embeddings,
        persist_directory = str(CHROMA_DIR),
    )
    return vectorstore.as_retriever(search_kwargs = {"k":k})