"""The app under test: a tiny RAG customer-support bot (free LLMs)."""
import os
import re
from pathlib import Path

from llm import APP_PROVIDER, chat

KB = [l.strip() for l in Path(__file__).with_name("policies.txt").read_text().splitlines() if l.strip()]
STOP = {"what", "is", "the", "a", "an", "do", "does", "you", "i", "my", "how", "when", "to",
        "of", "in", "on", "for", "and", "are", "can", "your", "it", "be", "by", "or", "this"}


def _tokens(text: str):
    """Lowercase words minus stopwords, crude plural strip (refunds -> refund)."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w[:-1] if len(w) > 3 and w.endswith("s") else w for w in words if w not in STOP}


def retrieve_policies(query: str, k: int = 1):
    if os.getenv("BREAK_RETRIEVER") == "1":  # simulated retrieval bug
        return [KB[3], KB[4]]
    q = _tokens(query)
    return sorted(KB, key=lambda d: len(q & _tokens(d)), reverse=True)[:k]


def generate_answer(query: str, context_docs: list):
    context = "\n".join(f"- {d}" for d in context_docs)
    prompt = ("Answer the question using ONLY the context below. "
              "If the answer is not in the context, say you don't know.\n\n"
              f"Context:\n{context}\n\nQuestion: {query}")
    return chat(APP_PROVIDER, prompt, system="You are a concise customer-support bot.")


def support_bot(query: str):
    docs = retrieve_policies(query)
    return generate_answer(query, docs), docs
