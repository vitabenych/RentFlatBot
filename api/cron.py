from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def dummy_check_channels():
    print("Перевіряю канали... (сюди підключиш Telethon пізніше)")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(dummy_check_channels, "interval", minutes=30)
    scheduler.start()
