from fastapi import FastAPI, HTTPException
import asyncpg
from api.routes import router
import os
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Завантажує змінні з .env

app = FastAPI()

# Ініціалізація OpenAI-клієнта з ключем з .env
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app.include_router(router, prefix="/api")

# Змінна підключення до БД
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://rentuser:010505@localhost:5432/rentflatdb"
)

# Модель для оголошення
class Apartment(BaseModel):
    text: str
    price: Optional[float] = None
    district: Optional[str] = None
    area: Optional[float] = None
    photos: Optional[List[str]] = None
    contacts: Optional[str] = None
    date: Optional[datetime] = None

# Модель для прийому тексту оголошення у AI-ендпоінті
class ListingText(BaseModel):
    text: str

# Підключення до бази при старті
@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)

# Закриття підключення при зупинці
@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

# Тестовий endpoint
@app.get("/")
async def root():
    return {"message": "Hello from RentFlatBot"}

# Endpoint для додавання оголошення
@app.post("/add_listing/")
async def add_listing(apartment: Apartment):
    query = """
        INSERT INTO apartments (text, price, district, area, photos, contacts, date)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (text) DO NOTHING
        RETURNING id;
    """
    async with app.state.db.acquire() as conn:
        result = await conn.fetchrow(
            query,
            apartment.text,
            apartment.price,
            apartment.district,
            apartment.area,
            apartment.photos,
            apartment.contacts,
            apartment.date,
        )
        if not result:
            raise HTTPException(status_code=409, detail="Duplicate listing detected")
        return {"id": result["id"], "message": "Listing added successfully"}

# ✅ Функція для парсингу оголошення через OpenAI (оновлений синтаксис)
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
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ти помічник, який витягує дані з оголошень про квартири."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=400,
    )

    result = response.choices[0].message.content.strip()

    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        data = {}
    return data

# Ендпоінт для парсингу тексту оголошення через AI
@app.post("/parse_listing/")
async def parse_listing_endpoint(listing: ListingText):
    data = await parse_listing_with_ai(listing.text)
    if not data:
        raise HTTPException(status_code=400, detail="Не вдалося розпізнати дані")
    return data
