import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Diretórios principais do projeto (baseados na raiz do projeto)
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VECTOR_DB_DIR = DATA_DIR / "vector_db"

# Garantindo que as pastas de dados existam
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

# Configurações de API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurações do RAG
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 500
