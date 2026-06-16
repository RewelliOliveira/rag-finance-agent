import os

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("OPENAI_API_KEY")[:10] + "...")

PASTE_BASE = "database"

def create_db():
    documents = load_documents()
    chunks = split_chunks(documents)
    vectorize_chunks(chunks)

def load_documents():
    charger =  PyPDFDirectoryLoader(PASTE_BASE, glob="*.pdf")
    documents = charger.load()
    return documents

def split_chunks(documents):
    documents_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True
    )

    chunks = documents_splitter.split_documents(documents)
    print(len(chunks))
    return chunks

def vectorize_chunks(chunks):
    db = Chroma.from_documents(chunks, OpenAIEmbeddings(model="text-embedding-3-small"), persist_directory="db_local")
    print("Banco de dados criado")

create_db()

# trocar o pypdf pelo pymupdf
# Camelot ou Tabula-py
# Unstructured.io
# LangGraph

# Para não depender apenas de PDFs estáticos, é legal dar 
# aos agentes a capacidade de buscar cotações e taxas em tempo real.

# yfinance: Para buscar histórico de preços e cotações de ações/FIIs brasileiras 
# (basta adicionar o sufixo .SA, ex: PETR4.SA).

# python-bcb: Uma biblioteca maravilhosa para buscar dados do Banco 
# Central do Brasil (Taxa Selic, IPCA), essencial para avaliar renda fixa ou custo de oportunidade.

# LangSmith: Ferramenta da própria LangChain para rastrear e debugar 
# as chamadas do LLM. Para o seu TCC, usar o LangSmith vai te dar
# métricas e gráficos lindos sobre o desempenho e os custos do seu RAG 
# para colocar no documento final.