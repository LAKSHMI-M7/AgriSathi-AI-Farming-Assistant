import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

print("API KEY:", os.getenv("GROQ_API_KEY"))

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are a farming assistant."},
        {"role": "user", "content": "What crop is suitable for Kerala climate?"}
    ]
)

print(response.choices[0].message.content)
