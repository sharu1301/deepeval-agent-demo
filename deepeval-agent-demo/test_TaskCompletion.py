"""Use case A: single LLM test case (matches the course layout).
Run: deepeval test run test_TaskCompletion.py"""
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, ContextualRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

from llm import JUDGE
from rag_agent import support_bot


def test_refund_window():
    query = "What is the refund window?"
    actual_output, retrieval_context = support_bot(query)
    print("\nQ:", query, "\nA:", actual_output)

    test_case = LLMTestCase(
        input=query,
        actual_output=actual_output,
        retrieval_context=retrieval_context,
        expected_output="Items can be returned within 30 days of delivery.",
    )
    assert_test(test_case, [
        AnswerRelevancyMetric(threshold=0.7, model=JUDGE, async_mode=False),
        FaithfulnessMetric(threshold=0.7, model=JUDGE, async_mode=False),
        ContextualRelevancyMetric(threshold=0.3, model=JUDGE, async_mode=False),
    ], run_async=False)