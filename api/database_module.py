import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://rentuser:010505@localhost:5432/rentflatdb"
)

db_pool = None

async def connect_to_db():
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)

async def close_db():
    if db_pool:
        await db_pool.close()

async def add_listing_to_db(apartment_data: dict):
    query = """
        INSERT INTO apartments (text, price, district, area, photos, contacts, date)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (text) DO NOTHING
        RETURNING id;
    """
    async with db_pool.acquire() as conn:
        result = await conn.fetchrow(
            query,
            apartment_data.get("text"),
            apartment_data.get("price"),
            apartment_data.get("district"),
            apartment_data.get("area"),
            apartment_data.get("photos"),
            apartment_data.get("contacts"),
            apartment_data.get("date"),
        )
        return result
