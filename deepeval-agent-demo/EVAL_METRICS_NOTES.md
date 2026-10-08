# AI evaluation metrics (what each one checks)
| Metric | Question it answers | Needs |
|---|---|---|
| Answer Relevancy | Does the answer address the question? | input, output |
| Faithfulness | Is the answer grounded in the retrieved context (no hallucination)? | output, retrieval_context |
| Contextual Relevancy | Is the retrieved context relevant to the question? | input, retrieval_context |
| Contextual Precision | Are the most relevant chunks ranked first? | input, expected_output, retrieval_context |
| Contextual Recall | Did retrieval cover everything in the expected answer? | expected_output, retrieval_context |
| G-Eval (custom) | Any rule you write in plain English (e.g. Correctness) | your choice |

Reading failures: low Contextual metrics => fix the retriever. Low Faithfulness with good context => fix the prompt/LLM.
