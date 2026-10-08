"""Run the app WITHOUT any evaluation: quick smoke test.  python agent_plain.py"""
from rag_agent import support_bot

for q in ["What is the refund window?", "Is shipping free?", "Do you ship to Mars?"]:
    answer, docs = support_bot(q)
    print(f"\nQ: {q}\nA: {answer}\nRetrieved: {[d[:30] + '...' for d in docs]}")
