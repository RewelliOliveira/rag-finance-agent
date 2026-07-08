import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="RAG Finance Agent CLI - Assistente Financeiro IA")
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Executa a extração de PDFs (com PyMuPDF/Pandas) e indexa no banco vetorial Chroma."
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Envia uma pergunta financeira ou dúvida sobre os documentos para o agente responder."
    )
    
    args = parser.parse_args()
    
    if args.ingest:
        from src.database.ingest import run_ingestion
        run_ingestion()
    elif args.query:
        from src.agents.assistant import get_agent_executor
        print(f"\n[Agente] Processando pergunta: '{args.query}'...\n")
        executor = get_agent_executor()
        try:
            response = executor.invoke({"input": args.query})
            print("\n--- RESPOSTA DO AGENTE FINANCEIRO ---")
            print(response.get("output", "Não foi possível obter uma resposta estruturada."))
        except Exception as e:
            print(f"\nErro durante a execução do agente: {str(e)}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()