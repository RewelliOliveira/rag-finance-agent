import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import config

def inspect_csv():
    file_path = config.RAW_DATA_DIR / "TaxaReferencia_PRE_20260707.csv"

    df = pd.read_csv(file_path, sep=";", encoding="latin-1")

    print(f"Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
    print(f"\nNomes das colunas:\n{list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nPrimeiras 10 linhas:\n")
    print(df.head(300).to_string())
    print(f"\nResumo Estatístico:\n")
    print(df.describe())

if __name__ == "__main__":
    inspect_csv()
