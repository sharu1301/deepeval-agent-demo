# deepeval-agent-demo
Evaluating a RAG customer-support bot with DeepEval using FREE LLMs (Groq / Gemini / Ollama).

## 📸 Evaluation Evidence

### 1. The App Working
*Notice the bot correctly says "I don't know" for the out-of-scope "Mars" question.*
![App Working] <img width="861" height="423" alt="App_Working png" src="https://github.com/user-attachments/assets/db1c8d5d-5af2-482f-8b34-b6357ac8d432" />


### 2. Basic Test Case Passing
*Answer Relevancy, Faithfulness, and Contextual Relevancy all score 1.0.*
![Basic Test] <img width="1305" height="746" alt="Basic_Test_TaskCompletion png" src="https://github.com/user-attachments/assets/5b686dd2-726b-4c89-a4d5-80e015dff522" />


### 3. Golden Dataset Regression Suite
*85.7% Pass Rate. The single failure is the Mars question, proving the retrieval metrics correctly flag a lack of data.*
![Golden Dataset] <img width="1312" height="701" alt="Golden_Dataset_Regression png" src="https://github.com/user-attachments/assets/c4fafb9b-d4c9-4230-8512-c6b985a42779" />


### 4. Trace-Level Normal Execution
*Both the Retriever (Contextual Relevancy) and Generator (Faithfulness) pass 100%.*
![Trace Normal] <img width="1310" height="880" alt="Trace_Normal1 png" src="https://github.com/user-attachments/assets/0a337e31-4bce-4aba-95ba-68f2eefc8c1e" />
<img width="1377" height="352" alt="Trace_Normal2 png" src="https://github.com/user-attachments/assets/54fffc07-4fe8-42ea-8bd8-cf63d471ed2b" />



### 5. Trace-Level Root Cause Analysis (Broken Retriever)
*I simulated a retrieval bug. Faithfulness stays at 1.0 (the LLM is perfect), but Contextual Relevancy crashes to 0.12. This isolates the bug to the retriever component.*
![Trace Broken] <img width="1920" height="2137" alt="Trace_Root_Cause_Broken png" src="https://github.com/user-attachments/assets/a87505c6-78e0-4c44-988f-45d443cedfec" />


### 6. Custom G-Eval Metric (Code Walkthrough)
*Note: Screenshot pending due to API free-tier limits. Code is in `test_GEval.py`.*
![G-Eval Metric] <img width="1534" height="6288" alt="Custom_GEval_Metric png" src="https://github.com/user-attachments/assets/f926cef9-01fb-4c37-be61-98a0b9e62c10" />


## Setup (Windows)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
