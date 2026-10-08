"""Use case C: trace-level evaluation (retriever and generator scored separately).
Run:  python run_tracing.py
Root cause demo:  set BREAK_RETRIEVER=1   then   python run_tracing.py"""
import json
from pathlib import Path

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.evaluate.configs import AsyncConfig

from agent_instrumented import traced_rag_app

if __name__ == "__main__":
    data = json.loads(Path(__file__).with_name("goldens.json").read_text())[:4]
    dataset = EvaluationDataset(goldens=[Golden(input=d["input"], expected_output=d["expected_output"])
                                         for d in data])
    for golden in dataset.evals_iterator(async_config=AsyncConfig(run_async=False)):
        traced_rag_app(golden.input)
