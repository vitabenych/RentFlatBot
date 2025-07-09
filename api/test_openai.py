import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, world!"}],
        max_tokens=5
    )
    print("API key працює. Відповідь від OpenAI:")
    print(response.choices[0].message.content)
except Exception as e:
    print("Щось пішло не так:")
    print(e)
