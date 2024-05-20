import logging
import os
from aiohttp import web
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from bot import register_handlers

load_dotenv()

TOKEN = os.getenv('TOKEN')
WEBHOOK_HOST = 'https://bbbb-alpha.vercel.app/'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

register_handlers(dp)  # Регистрация обработчиков

async def on_startup(app):
    logging.info('Starting up...')
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook URL: {WEBHOOK_URL}")

async def on_shutdown(app):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    logging.warning('Bye!')

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

def handler(request, *args):
    return app._handle(request)

if __name__ == '__main__':
    web.run_app(app)
