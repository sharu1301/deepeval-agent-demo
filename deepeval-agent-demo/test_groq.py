import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=key
)

# WE ARE HARDCODING THE NEW MODEL HERE
MODEL_NAME = "openai/gpt-oss-20b"
print(f"--- DEBUG: USING MODEL '{MODEL_NAME}' ---")

try:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": "Say 'API is working'"}]
    )
    print("SUCCESS:", response.choices[0].message.content)
except Exception as e:
    print("\nRAW ERROR:", e)