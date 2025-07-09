import json
import os
from openai import OpenAI
import asyncio

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

async def parse_listing(text: str) -> dict:
    prompt = f"""
    Витягни з тексту оголошення про квартиру такі поля у форматі JSON:
    - price (ціна, число)
    - district (район, текст)
    - area (площа в кв.м, число)
    - photos (список URL, якщо є)
    - contacts (контактний телефон чи email)
    - date (дата у форматі YYYY-MM-DD, якщо є)

    Текст оголошення: \"\"\"{text}\"\"\"

    Відповідь тільки у форматі JSON.
    """

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ти помічник, який витягує дані з оголошень про квартири."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=300,
    )

    result = response.choices[0].message.content.strip()

    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        data = {}

    # Додатково можна додати, щоб у полі "text" був оригінальний текст оголошення
    data["text"] = text

    return data
