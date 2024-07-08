import logging
from fastapi import FastAPI, Request
from aiogram import types, Dispatcher, Bot
from handlers import dp, bot
import os
from config import TOKEN,POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_DATABASE,POSTGRES_HOST  
from db import Database
from starlette.middleware.cors import CORSMiddleware
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из .env файла


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://bbbb-alpha.vercel.app{WEBHOOK_PATH}"

@app.on_event("startup")
async def on_startup():
    logger.info("Starting up application")
    await bot.set_webhook(url=WEBHOOK_URL)
    logger.info(f"Webhook URL set to: {WEBHOOK_URL}")

@app.get("/")
async def read_root():
    return {"message": "Webhook is set and running"}

@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    try:
        await Database.connect(
            user=POSTGRES_USER, 
            password=POSTGRES_PASSWORD, 
            database=POSTGRES_DATABASE, 
            host=POSTGRES_HOST
        )
    except Exception as e:
        logger.error(f"Failed to connect to database:{e}")
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
app=app
