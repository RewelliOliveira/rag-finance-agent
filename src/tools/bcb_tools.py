import requests
import pandas as pd
from langchain_core.tools import tool

@tool
def get_selic_rate() -> str:
    """Busca a taxa Selic acumulada nos últimos 30 dias diretamente do Sistema Gerenciador de Séries 
    Temporais (SGS) do Banco Central do Brasil, retornando o histórico diário formatado.
    
    Returns:
        str: Dados formatados da taxa Selic diária.
    """
    try:
        # Série 11: Taxa de juros - Selic acumulada no dia (% a.a.)
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/30?formato=json"
        response = requests.get(url)
        if response.status_code != 200:
            return "Erro de conexão com o sistema do Banco Central do Brasil."
            
        data = response.json()
        df = pd.DataFrame(data)
        
        # Tratamento de dados com Pandas
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df['valor'] = pd.to_numeric(df['valor'])
        
        # Ajusta exibição
        df.columns = ['Data', 'Taxa Diária (% a.a.)']
        df['Data'] = df['Data'].dt.date
        
        return "\nÚltimos 30 registros da Taxa Selic Diária:\n" + df.to_string(index=False)
    except Exception as e:
        return f"Erro ao obter dados da Taxa Selic do Banco Central: {str(e)}"
