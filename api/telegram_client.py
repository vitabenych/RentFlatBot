import os
from pyrogram import Client
from api.actions import parse_and_save_listing  # твоя функція, яка обробляє текст

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")

app = Client("my_session", api_id=API_ID, api_hash=API_HASH)

@app.on_message()
async def handle_message(client, message):
    # Фільтруємо по каналу за username
    if message.chat and message.chat.username == "orendakvarturlviv" and message.text:
        print(f"Отримано повідомлення: {message.text}")
        # Записуємо текст у файл у кодуванні UTF-8
        with open("messages.txt", "a", encoding="utf-8") as f:
            f.write(message.text + "\n")
        await parse_and_save_listing(message.text)

if __name__ == "__main__":
    app.run()
