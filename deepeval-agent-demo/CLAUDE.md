# Project notes for AI coding assistants
- Purpose: demo of evaluating a RAG support bot with DeepEval, using FREE LLMs (Ollama / Groq / Gemini).
- App: `rag_agent.py` (retrieve over `policies.txt` -> generate). Providers + judge: `llm.py`.
- Tests: `test_*.py`, run with `deepeval test run <file>`. Trace evals: `python run_tracing.py`.
- Config via `.env` (never commit it). `BREAK_RETRIEVER=1` simulates a retrieval bug.
- Judge metrics are sequential (`async_mode=False`) to respect free-tier rate limits.
