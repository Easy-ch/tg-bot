from fastapi import FastAPI, Request
from aiogram import types, Dispatcher, Bot
from bot import dp, bot,register_handlers
from dotenv import load_dotenv
import os
load_dotenv()
register_handlers(dp)
app = FastAPI()
TOKEN = os.getenv('TOKEN')
WEBHOOK_HOST = 'https://bbbb-alpha.vercel.app/'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    telegram_update = types.Update(await request.json())
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
@app.get("/")
async def root():
    return {"message": "Bot webhook is running"}
