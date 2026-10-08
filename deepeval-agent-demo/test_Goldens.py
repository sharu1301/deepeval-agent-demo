"""Use case B: golden dataset = regression suite (5 metrics incl. RAG retrieval metrics).
Run: deepeval test run test_Goldens.py        (fewer cases: set GOLDEN_LIMIT=3)"""
import json
import os
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.metrics import (AnswerRelevancyMetric, ContextualPrecisionMetric,
                              ContextualRecallMetric, ContextualRelevancyMetric, FaithfulnessMetric)
from deepeval.test_case import LLMTestCase

from llm import JUDGE
from rag_agent import support_bot

GOLDENS = json.loads(Path(__file__).with_name("goldens.json").read_text())
if os.getenv("GOLDEN_LIMIT"):
    GOLDENS = GOLDENS[: int(os.environ["GOLDEN_LIMIT"])]


def metric(cls, threshold):
    return cls(threshold=threshold, model=JUDGE, async_mode=False)


@pytest.mark.parametrize("golden", GOLDENS, ids=[g["input"][:40] for g in GOLDENS])
def test_golden(golden):
    answer, docs = support_bot(golden["input"])
    tc = LLMTestCase(input=golden["input"], actual_output=answer,
                     expected_output=golden["expected_output"], retrieval_context=docs)
    assert_test(tc, [metric(AnswerRelevancyMetric, 0.7), metric(FaithfulnessMetric, 0.7),
                     metric(ContextualRelevancyMetric, 0.6), metric(ContextualPrecisionMetric, 0.6),
                     metric(ContextualRecallMetric, 0.6)], run_async=False)
