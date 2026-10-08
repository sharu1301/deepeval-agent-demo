"""Same app with DeepEval tracing: each component gets its own metric (trace-level testing)."""
from deepeval.metrics import ContextualRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from deepeval.tracing import observe, update_current_span

from llm import JUDGE
from rag_agent import generate_answer, retrieve_policies

retriever_metric = ContextualRelevancyMetric(threshold=0.6, model=JUDGE, async_mode=False)
generator_metric = FaithfulnessMetric(threshold=0.7, model=JUDGE, async_mode=False)


@observe(metrics=[retriever_metric])
def traced_retrieve(query: str):
    docs = retrieve_policies(query)
    update_current_span(test_case=LLMTestCase(
        input=query, actual_output="\n".join(docs), retrieval_context=docs))
    return docs


@observe(metrics=[generator_metric])
def traced_generate(query: str, docs):
    answer = generate_answer(query, docs)
    update_current_span(test_case=LLMTestCase(
        input=query, actual_output=answer, retrieval_context=docs))
    return answer


@observe()
def traced_rag_app(query: str):
    return traced_generate(query, traced_retrieve(query))
