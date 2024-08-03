import logging
from fastapi import FastAPI, Request
from aiogram import types, Dispatcher, Bot
from handlers import dp, bot
from config import TOKEN, POSTGRES_DATABASE, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER
from db import Database, Course, Order
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из .env файла

app = FastAPI()

WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://bbbb-alpha.vercel.app{WEBHOOK_PATH}"

async def init():
    logger.info("Starting up application")
    try:
        await Database.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD, database=POSTGRES_DATABASE, host=POSTGRES_HOST)
        await Course.create_table()
        await Order.create_table()
        await bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook URL set to: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")

async def init():
    logger.info("Starting up application")
    try:
        await Database.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD, database=POSTGRES_DATABASE, host=POSTGRES_HOST)
        await Course.create_table()
        await Order.create_table()
        await bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook URL set to: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")

@app.on_event("startup")
def on_startup():
    asyncio.create_task(init())
    logger.info('Create_task')


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

async def shutdown():
    await Database.close()
    await bot.session.close()

@app.on_event("shutdown")


async def on_shutdown():
    await Database.close()
    await bot.session.close()   


