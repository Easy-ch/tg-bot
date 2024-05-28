import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os
from dotenv import load_dotenv
from bot import register_handlers,bot,dp
import json
# Загрузка переменных окружения из .env файла
load_dotenv()
register_handlers(dp)
# Инициализация бота и диспетчера
API_TOKEN = os.getenv('TOKEN')
WEBHOOK_HOST = 'https://bbbb-alpha.vercel.app'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'  # IP-адрес для запуска веб-приложения
WEBAPP_PORT = 80  # Порт для запуска веб-приложения

logging.basicConfig(level=logging.INFO)


async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown():
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await bot.session.close()
    logging.warning('Bye!')

async def handle(request):
    try:
        update_json =await request.json()
        update = types.Update(**update_json)
        await dp.feed_update(bot,update)
        return web.Response(text="OK")
    except Exception as e:
        logging.error(f"Failed to process update: {e}")
        return web.Response(status=500, text="Internal Server Error")

if __name__ == '__main__':
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
