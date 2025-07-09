from api.ai_module import parse_listing_with_ai
from api.database_module import add_listing_to_db

async def add_listing(apartment_data: dict):
    result = await add_listing_to_db(apartment_data)
    if not result:
        return {"message": "Duplicate listing detected"}
    return {"id": result["id"], "message": "Listing added successfully"}

async def parse_and_save_listing(text: str):
    try:
        parsed_data = await parse_listing_with_ai(text)
        parsed_data["text"] = text 
        await add_listing_to_db(parsed_data)
        print("✅ Збережено в базу даних")
    except Exception as e:
        print(f"❌ Помилка під час збереження: {e}")
