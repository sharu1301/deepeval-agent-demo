"""Interactive CLI chatbot around the RAG agent.  python chatbot.py   (type 'quit' to exit)"""
from rag_agent import support_bot

if __name__ == "__main__":
    print("Acme support bot. Ask about refunds, shipping, warranty, support hours, passwords.")
    while True:
        q = input("\nYou: ").strip()
        if q.lower() in {"quit", "exit", ""}:
            break
        answer, docs = support_bot(q)
        print("Bot:", answer)
