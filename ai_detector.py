import os
from dotenv import load_dotenv
from openai import OpenAI

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)