import os
import glob
import fitz
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from src import config

def run_ingestion():
    """Função principal para executar o processo de ingestão de dados."""
    print("Iniciando processo de ingestão...")
    documents = load_documents()
    if not documents:
        print("Nenhum documento encontrado para ingestão.")
        return
        
    chunks = split_chunks(documents)
    vectorize_chunks(chunks)

def load_documents():
    """Lê PDFs brutas, extrai texto e tabelas (com Pandas) e retorna Documentos LangChain."""
    documents = []
    pdf_paths = glob.glob(os.path.join(config.RAW_DATA_DIR, "*.pdf"))
    
    for pdf_path in pdf_paths:
        file_name = os.path.basename(pdf_path)
        print(f"Lendo PDF: {file_name}")
        
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"Erro ao abrir o PDF {file_name}: {e}")
            continue
            
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            try:
                tables = page.find_tables()
                if tables.tables:
                    print(f"  -> Encontrada(s) {len(tables.tables)} tabela(s) na página {page_num + 1}")
                    for i, table in enumerate(tables.tables):
                        df = table.to_pandas()
                        markdown_table = df.to_markdown(index=False)
                        text += f"\n\n### Tabela {i + 1} extraída da página:\n{markdown_table}\n"
            except Exception as e:
                print(f"  -> Erro ao extrair tabela da página {page_num + 1}: {e}")
                
            if text.strip():
                doc_obj = Document(
                    page_content=text,
                    metadata={
                        "source": file_name,
                        "page": page_num + 1
                    }
                )
                documents.append(doc_obj)
                
        doc.close()
        
    return documents

def split_chunks(documents):
    """Divide os documentos carregados em chunks menores."""
    documents_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True
    )

    chunks = documents_splitter.split_documents(documents)
    print(f"Total de chunks gerados: {len(chunks)}")
    return chunks

def vectorize_chunks(chunks):
    """Gera as embeddings e salva no banco de dados vetorial Chroma."""
    embeddings = OpenAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        openai_api_key=config.OPENAI_API_KEY
    )
    
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=str(config.VECTOR_DB_DIR)
    )
    print("Banco de dados criado com sucesso e salvo em:", config.VECTOR_DB_DIR)

if __name__ == "__main__":
    run_ingestion()
