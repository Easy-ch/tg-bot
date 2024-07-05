import logging
from fastapi import FastAPI, Request
from aiogram import types, Dispatcher, Bot
from handlers import dp, bot
import os
from config import TOKEN   
from db import Database
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из .env файла


app = FastAPI()

WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://7c05-188-243-182-2.ngrok-free.app{WEBHOOK_PATH}"

@app.on_event("startup")
async def on_startup():
    logger.info("Starting up application")
    try:
        await Database.connect(
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database=os.getenv('POSTGRES_DATABASE'),
            host=os.getenv('POSTGRES_HOST')
        )
        webhook_info = await bot.get_webhook_info()
        await bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook URL set to: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Failed to connect to database or set webhook: {e}")

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
    await Database.close()
    await bot.session.close()   

# Экспорт приложения для Vercel


