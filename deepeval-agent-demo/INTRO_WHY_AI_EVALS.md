# Why AI evals?
- LLM output is non-deterministic, so `assert x == y` does not work.
- We score meaning with an LLM judge against metrics, on a fixed golden dataset (regression suite).
- Trace-level tests score each component (retriever, generator) so we can find root causes fast.
- Caveat: a free/small judge model gives indicative, not authoritative, scores.
