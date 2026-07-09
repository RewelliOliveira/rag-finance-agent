# RAG Finance Agent

Este projeto consiste em um assistente de análise financeira inteligente baseado em modelos de linguagem de grande porte (LLMs). Ele utiliza a arquitetura RAG (Retrieval-Augmented Generation) integrada a ferramentas de manipulação de dados locais e consultas a APIs de mercado em tempo real.

O projeto foi projetado com foco em modularidade, separação de responsabilidades e escalabilidade, seguindo boas práticas de desenvolvimento de software e IA.

---

## Funcionalidades Principais

- **RAG Híbrido (Texto e Tabelas)**: Processamento de relatórios em formato PDF com extração inteligente de texto e conversão de tabelas em DataFrames do Pandas, posteriormente estruturadas em Markdown para preservação de contexto no banco vetorial.
- **Integração com Yahoo Finance**: Busca automática de histórico de cotações, preços de fechamento e volume de negociação de ativos nacionais e internacionais.
- **Integração com Banco Central do Brasil (SGS)**: Busca de indicadores macroeconômicos em tempo real, como o histórico de cotação da Taxa Selic diária.
- **Análise Analítica com Pandas**: Capacidade para o agente mapear e extrair dados estatísticos descritivos de tabelas locais nos formatos CSV e Parquet.
- **Interface de Linha de Comando (CLI)**: Entrada única para disparar tarefas de indexação de novos documentos ou realizar consultas ao assistente.

---

## Tecnologias e Ferramentas Utilizadas

- **Python**: Linguagem de programação base do ecossistema.
- **LangChain / LangChain Classic**: Framework de orquestração para estruturar o agente de tomada de decisões e a integração das ferramentas de chamada (tools).
- **OpenAI API**: Modelos GPT-4o-mini (para raciocínio cognitivo) e Text-Embedding-3-Small (para a geração dos vetores dos documentos).
- **ChromaDB**: Banco de dados vetorial de alta performance para armazenamento local e recuperação de dados por similaridade de cosseno.
- **PyMuPDF**: Biblioteca para manipulação de arquivos PDF e detecção de tabelas estruturadas nas páginas.
- **Pandas**: Biblioteca analítica de alta performance para manipulação e estruturação de séries temporais financeiras e estatísticas.
- **Yahoo Finance (yfinance)**: Biblioteca de extração de dados históricos de ativos cotados em bolsas.
- **Requests**: Biblioteca HTTP para integração direta à API do Sistema Gerenciador de Séries Temporais (SGS) do Banco Central do Brasil.
- **Tabulate**: Biblioteca de formatação auxiliar para converter DataFrames em tabelas de Markdown amigáveis ao LLM.

---

## Estrutura do Projeto

O código-fonte está estruturado de forma modular dentro do pacote `src`:

```text
rag-finance-agent/
│
├── data/                       # Armazenamento de dados do sistema
│   ├── raw/                    # Documentos PDF e planilhas originais inseridos pelo usuário
│   ├── processed/              # Tabelas geradas e estruturadas pelo Pandas
│   └── vector_db/              # Armazenamento físico do banco de dados ChromaDB
│
├── src/                        # Código-fonte principal da aplicação
│   ├── config.py               # Configurações globais, caminhos físicos e validação do .env
│   ├── database/
│   │   ├── ingest.py           # Pipeline de leitura de PDFs e ingestão no ChromaDB
│   │   └── retriever.py        # Inicializador e configurações do recuperador vetorial
│   ├── tools/
│   │   ├── yfinance_tools.py   # Ferramenta para cotações do Yahoo Finance
│   │   ├── bcb_tools.py        # Ferramenta para dados de juros do Banco Central do Brasil
│   │   └── pandas_analyst.py   # Ferramenta para análise descritiva de dados tabulares locais
│   └── agents/
│       ├── prompts.py          # Armazenamento das instruções do sistema (System Prompt)
│       └── assistant.py        # Orquestrador do LangChain Agent Executor
│
├── scripts/                    # Scripts utilitários de diagnóstico para desenvolvimento
│   ├── inspect_tables.py       # Exibe as tabelas detectadas pelo PyMuPDF em DataFrames Pandas
│   └── inspect_csv.py          # Exibe o conteúdo de um arquivo CSV específico usando Pandas
│
├── main.py                     # CLI e ponto de entrada da aplicação
├── requirements.txt            # Dependências estruturadas do projeto
└── .env                        # Chaves e credenciais de acesso locais privadas
```

---

## Instalação e Configuração

### Pré-requisitos
- Python instalado no sistema.
- Um arquivo de credenciais `.env` configurado na raiz do projeto contendo a chave da OpenAI:
  ```env
  OPENAI_API_KEY=sua_chave_aqui
  ```

### Procedimento de Instalação

1. Clone o repositório para o seu ambiente local.
2. Crie e ative um ambiente virtual de sua preferência (ex: venv):
   ```powershell
   # Criação
   python -m venv venv
   # Ativação (Windows PowerShell)
   .\venv\Scripts\Activate.ps1
   ```
3. Instale as dependências listadas no arquivo `requirements.txt`:
   ```powershell
   pip install -r requirements.txt
   ```

---

## Como Executar

O projeto possui uma interface em CLI simples. Certifique-se de estar com a pasta venv ativada no seu terminal antes de executar os comandos.

### Ingestão de Documentos
Para indexar os documentos PDFs localizados na pasta `data/raw/` para o banco de dados vetorial:
```powershell
python main.py --ingest
```

### Consulta ao Assistente Financeiro
Para interagir com o agente financeiro estruturado e enviar perguntas para o modelo com suporte a ferramentas:
```powershell
python main.py --query "Qual foi a taxa Selic acumulada diária nos últimos 30 dias?"
```
```powershell
python main.py --query "O que o regulamento do Balcão B3 diz sobre o papel da B3 como administradora?"
```
