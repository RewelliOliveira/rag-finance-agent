from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

from src import config
from src.agents.prompts import SYSTEM_PROMPT
from src.database.retriever import get_retriever
from src.tools.yfinance_tools import get_stock_history
from src.tools.bcb_tools import get_selic_rate
from src.tools.pandas_analyst import list_processed_datasets, get_dataset_summary

@tool
def search_documents(query: str) -> str:
    """Busca trechos relevantes e fatos de documentos e regulamentos locais em PDF relacionados à pergunta.
    
    Args:
        query (str): Termos de busca ou pergunta para encontrar nos documentos.
        
    Returns:
        str: Fragmentos de texto relevantes dos documentos.
    """
    try:
        retriever = get_retriever()
        docs = retriever.invoke(query)
        
        results = []
        for doc in docs:
            source = doc.metadata.get("source", "desconhecido")
            page = doc.metadata.get("page", "?")
            results.append(f"[Documento: {source} | Página: {page}]\n{doc.page_content}\n---")
            
        return "\n\n".join(results) if results else "Nenhum trecho relevante encontrado nos PDFs."
    except Exception as e:
        return f"Erro ao realizar busca vetorial nos documentos: {str(e)}"

def get_agent_executor():
    """Configura o LLM, as ferramentas e constrói o agente financeiro.
    
    Returns:
        AgentExecutor: O executor do agente pronto para responder perguntas.
    """
    tools = [
        search_documents,
        get_stock_history,
        get_selic_rate,
        list_processed_datasets,
        get_dataset_summary
    ]
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",  
        temperature=0,        
        openai_api_key=config.OPENAI_API_KEY
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
