import logging
import os
import json
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("No TOKEN provided")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

WEBHOOK_HOST = 'https://your-webhook-url'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Это бот.")

async def handle(request):
    body = await request.text()
    update = Update.parse_raw(body)
    await dp.process_update(update)
    return web.Response(status=200)

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f'Webhook set to {WEBHOOK_URL}')

async def on_shutdown(app):
    await bot.delete_webhook()

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=3000)
