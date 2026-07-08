import yfinance as yf
import pandas as pd
from langchain_core.tools import tool

@tool
def get_stock_history(ticker: str, period: str = "1mo") -> str:
    """Busca o histórico de cotações de um ativo pelo ticker (ex: PETR4.SA ou AAPL) e período.
    Usa o Pandas para formatar e resumir o retorno estruturado.
    
    Args:
        ticker (str): O símbolo do ativo financeiro (ações, fundos imobiliários, etc.).
        period (str): Período do histórico (1d, 5d, 1mo, 3mo, 6mo, 1y, ytd, max).
        
    Returns:
        str: Uma tabela contendo as datas, preços de fechamento e volume de transações.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        if df.empty:
            return f"Nenhum dado histórico encontrado para o ativo '{ticker}'."
            
        # Seleciona apenas as colunas mais importantes e limpa o índice
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.index = df.index.date  # Remove fuso horário e mantém apenas a data
        df = df.round(2)
        
        # Converte em string formatada do Pandas
        return f"\nHistórico de Cotações para {ticker} ({period}):\n" + df.to_string()
    except Exception as e:
        return f"Erro ao obter dados de cotações para o ativo {ticker}: {str(e)}"
