"""Use case D: custom G-Eval metric written in plain English.
Run: deepeval test run test_GEval.py"""
import json
import os
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from llm import JUDGE
from rag_agent import support_bot

GOLDENS = json.loads(Path(__file__).with_name("goldens.json").read_text())
if os.getenv("GOLDEN_LIMIT"):
    GOLDENS = GOLDENS[: int(os.environ["GOLDEN_LIMIT"])]

correctness = GEval(
    name="Correctness",
    criteria=("Determine whether the actual output is factually consistent with the expected "
              "output. Penalize contradictions and invented details. If the expected output says "
              "the bot should say it doesn't know, reward answers that admit uncertainty."),
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT,
                       LLMTestCaseParams.EXPECTED_OUTPUT],
    threshold=0.7, model=JUDGE, async_mode=False)


@pytest.mark.parametrize("golden", GOLDENS, ids=[g["input"][:40] for g in GOLDENS])
def test_correctness(golden):
    answer, docs = support_bot(golden["input"])
    tc = LLMTestCase(input=golden["input"], actual_output=answer,
                     expected_output=golden["expected_output"], retrieval_context=docs)
    assert_test(tc, [correctness], run_async=False)
