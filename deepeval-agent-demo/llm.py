"""Free LLM providers (Ollama / Groq / Gemini) + a DeepEval judge built on them."""
import json
import os
import re
import time

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from deepeval.models import DeepEvalBaseLLM

load_dotenv()

PROVIDERS = {
    "ollama": dict(base_url="http://localhost:11434/v1", key_env=None,
                   model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b")),
    "gemini": dict(base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                   key_env="GEMINI_API_KEY",
                   model=os.getenv("GEMINI_MODEL", "gemini-flash-latest")),
    "groq": dict(base_url="https://api.groq.com/openai/v1", key_env="GROQ_API_KEY",
                 model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")),
}
DEFAULT = os.getenv("LLM_PROVIDER", "ollama")
APP_PROVIDER = os.getenv("APP_PROVIDER") or DEFAULT
JUDGE_PROVIDER = os.getenv("JUDGE_PROVIDER") or DEFAULT
THROTTLE = float(os.getenv("CALL_DELAY", "0") or 0)


def chat(provider: str, prompt: str, system: str = "You are a helpful assistant.") -> str:
    cfg = PROVIDERS[provider]
    key = os.getenv(cfg["key_env"]) if cfg["key_env"] else "ollama"
    if not key:
        raise SystemExit(f"Set {cfg['key_env']} in .env for provider '{provider}'.")
    client = OpenAI(base_url=cfg["base_url"], api_key=key)
    last = None
    for attempt in range(6):  # retry with backoff: free tiers return 429 often
        try:
            if THROTTLE:
                time.sleep(THROTTLE)
            r = client.chat.completions.create(
                model=cfg["model"], temperature=0,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": prompt}])
            text = r.choices[0].message.content or ""
            return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
        except Exception as e:  # noqa: BLE001
            last = e
            wait = min(60, 5 * (attempt + 1))
            print(f"  [{provider}] call failed ({type(e).__name__}); retry in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"{provider} failed after retries: {last}")


class FreeJudge(DeepEvalBaseLLM):
    """DeepEval judge backed by any free OpenAI-compatible provider."""

    def __init__(self, provider: str):
        self.provider = provider
        self.model_name = f"{provider}:{PROVIDERS[provider]['model']}"
        super().__init__(self.model_name)

    def load_model(self):
        return None

    def generate(self, prompt: str, schema: BaseModel = None):
        if schema is None:
            return chat(self.provider, prompt)
        full = (prompt + "\n\nReturn ONLY valid JSON (no markdown fences, no commentary) "
                f"matching this JSON schema:\n{json.dumps(schema.model_json_schema())}")
        for _ in range(3):  # small local models sometimes break JSON
            m = re.search(r"\{.*\}", chat(self.provider, full), re.DOTALL)
            try:
                return schema(**json.loads(m.group(0)))
            except Exception:  # noqa: BLE001
                continue
        raise ValueError("Judge did not return valid JSON. Use a bigger model / hybrid setup.")

    async def a_generate(self, prompt: str, schema: BaseModel = None):
        return self.generate(prompt, schema)

    def get_model_name(self):
        return self.model_name


JUDGE = FreeJudge(JUDGE_PROVIDER)
