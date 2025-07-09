import asyncpg
from dotenv import load_dotenv
import os

DATABASE_URL = os.getenv("DATABASE_URL")
load_dotenv() 

db_pool = None

async def connect_to_db():
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)

async def close_db():
    if db_pool:
        await db_pool.close()

async def add_listing_to_db(listing: dict):
    query = """
        INSERT INTO apartments (text, price, district, area, photos, contacts, date)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (text) DO NOTHING
        RETURNING id;
    """
    async with db_pool.acquire() as conn:
        result = await conn.fetchrow(
            query,
            listing.get("text"),
            listing.get("price"),
            listing.get("district"),
            listing.get("area"),
            listing.get("photos"),
            listing.get("contacts"),
            listing.get("date"),
        )
        return result
