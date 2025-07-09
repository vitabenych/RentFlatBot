import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "твій_ключ_якщо_немає_в_середовищі"))

async def parse_listing_with_ai(text: str) -> dict:
    prompt = f"""
    Витягни з тексту оголошення про квартиру такі поля у форматі JSON:
    - price (число)
    - district (текст)
    - area (число)
    - photos (список URL)
    - contacts (контактний телефон або email)
    - date (у форматі YYYY-MM-DD)

    Текст оголошення: \"\"\"{text}\"\"\"

    Відповідь тільки у форматі JSON.
    """

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ти помічник, який витягує дані з оголошень про квартири."},
            {"role": "user", "content": prompt}
        ],
    )

    result = response.choices[0].message.content.strip()
    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        data = {}
    return data
