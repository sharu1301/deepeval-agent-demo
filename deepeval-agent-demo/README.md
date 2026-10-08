# deepeval-agent-demo
Evaluating a RAG customer-support bot with DeepEval using FREE LLMs.

## Setup (Windows)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Edit `.env` (set `LLM_PROVIDER`; add a free Groq/Gemini key, or use Ollama: install from ollama.com, `ollama pull qwen2.5:7b`).

## Run
| Use case | Command |
|---|---|
| Smoke test the app | `python agent_plain.py` |
| A. Single test case | `deepeval test run test_TaskCompletion.py` |
| B. Golden dataset | `deepeval test run test_Goldens.py` |
| C. Trace-level | `python run_tracing.py` |
| C2. Root cause | `set BREAK_RETRIEVER=1` then `python run_tracing.py` |
| D. G-Eval custom metric | `deepeval test run test_GEval.py` |
| Chat with the bot | `python chatbot.py` |

Free-quota tips: `set GOLDEN_LIMIT=3`; `CALL_DELAY=3` in `.env` if you see 429s.
