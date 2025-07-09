import os
from pyrogram import Client, filters
from api.actions import parse_and_save_listing

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")

app = Client("my_session", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.chat("orendakvarturlviv"))
async def handle_message(client, message):
    if message.text:
        print(f"📩 Нова подія: {message.text}")
        try:
            await parse_and_save_listing(message.text)
        except Exception as e:
            print(f"❌ Помилка збереження: {e}")

if __name__ == "__main__":
    app.run()
