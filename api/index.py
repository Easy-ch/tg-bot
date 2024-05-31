import logging
from fastapi import FastAPI, Request
from aiogram import types, Dispatcher, Bot
from bot import dp, bot, register_handlers
from dotenv import load_dotenv
import os
import asyncio
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из .env файла
load_dotenv()
register_handlers(dp)

app = FastAPI()
TOKEN = str(os.getenv('TOKEN'))
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://bbbb-alpha.vercel.app{WEBHOOK_PATH}"

@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
    logger.info(f"Webhook URL set to: {WEBHOOK_URL}")

@app.get("/")
async def read_root():
    return {"message": "Webhook is set and running"}

@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    try:
        logger.info("Received a POST request")
        update = await request.json()
        logger.info(f"Update received: {update}")
        telegram_update = types.Update(**update)
        Dispatcher.set_current(dp)
        Bot.set_current(bot)
        await dp.process_update(telegram_update)
        logger.info("Update processed successfully")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Failed to process update: {e}")
        return {"status": "error", "message": str(e)}

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()

# Экспорт приложения для Vercel
async def main():
    await asyncio.gather(
        app.startup(),
        app.main(),
        app.shutdown(),
        app.bot_webhook()
    )

if __name__ == '__main__':
    asyncio.run(main())

