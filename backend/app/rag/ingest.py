from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.config import DOCS_DIR,EMBEDDING_MODEL,CHROMA_DIR

def load_documents():
    """加载word文档"""
    docs = []
    for path in DOCS_DIR.glob("*.docx"):#遍历文档
        docs.extend(Docx2txtLoader(str(path)).load())
    return docs

def split_documents(docs):
    """按照要求切分word文档"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
        separators = ["\n\n", "\n", "。", "！", "？"]
    )
    return splitter.split_documents(docs)

def build_vector_store(chunks):
    """将文本转化为向量,存到向量库"""
    embeddings = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL)
    return Chroma.from_documents(
        documents = chunks,
        embedding = embeddings,
        persist_directory = str(CHROMA_DIR)
    )

def ingest():
    docs = load_documents()
    print(f"共加载{len(docs)}个文档")
    chunks = split_documents(docs)
    print(f"共切成{len(chunks)}个文本块")
    build_vector_store(chunks)

if __name__ == "__main__":
    ingest()
