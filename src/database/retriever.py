from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from src import config

def get_retriever():
    """Inicializa o banco de dados Chroma e retorna um objeto Retriever para buscar documentos."""
    embeddings = OpenAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        openai_api_key=config.OPENAI_API_KEY
    )
    
    db = Chroma(
        persist_directory=str(config.VECTOR_DB_DIR),
        embedding_function=embeddings
    )
    return db.as_retriever(search_kwargs={"k": 4})
