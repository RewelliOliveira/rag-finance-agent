import os
import glob
import pandas as pd
from langchain_core.tools import tool
from src import config

@tool
def list_processed_datasets() -> str:
    """Lista todos os arquivos de dados estruturados (CSVs e Parquet) disponíveis 
    no diretório de dados processados.
    
    Returns:
        str: Uma lista dos arquivos disponíveis com seus respectivos tamanhos.
    """
    files = glob.glob(os.path.join(config.PROCESSED_DATA_DIR, "*"))
    if not files:
        return "Nenhum arquivo de dados estruturados disponível no momento."
        
    file_list = []
    for file in files:
        file_name = os.path.basename(file)
        size = os.path.getsize(file)
        file_list.append(f"- {file_name} ({size / 1024:.2f} KB)")
        
    return "Arquivos de dados estruturados disponíveis:\n" + "\n".join(file_list)

@tool
def get_dataset_summary(filename: str) -> str:
    """Carrega um arquivo de dados estruturados do diretório de dados processados e 
    retorna um resumo estatístico e as primeiras linhas do arquivo via Pandas.
    
    Args:
        filename (str): O nome do arquivo a ser analisado (ex: 'dados.csv').
        
    Returns:
        str: O resumo das colunas, primeiras linhas e estatísticas descritivas (df.describe()).
    """
    try:
        file_path = os.path.join(config.PROCESSED_DATA_DIR, filename)
        if not os.path.exists(file_path):
            return f"Erro: O arquivo '{filename}' não foi encontrado em '{config.PROCESSED_DATA_DIR}'."
            
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif filename.endswith('.parquet') or filename.endswith('.pq'):
            df = pd.read_parquet(file_path)
        else:
            return "Erro: Formato de arquivo não suportado. Use apenas arquivos .csv ou .parquet."
            
        summary = f"--- Resumo de Dados: {filename} ---\n"
        summary += f"Tamanho: {df.shape[0]} linhas, {df.shape[1]} colunas\n\n"
        summary += "Primeiras 5 linhas:\n" + df.head().to_string() + "\n\n"
        summary += "Estatísticas Descritivas:\n" + df.describe(include='all').to_string()
        
        return summary
    except Exception as e:
        return f"Erro ao analisar o conjunto de dados {filename}: {str(e)}"
