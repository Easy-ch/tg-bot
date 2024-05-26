import logging
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os
from dotenv import load_dotenv
from bot import register_handlers,bot,dp
load_dotenv()
register_handlers(dp)

API_TOKEN =os.getenv('TOKEN') 
WEBHOOK_HOST = 'https://bbbb-alpha.vercel.app'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 80

logging.basicConfig(level=logging.INFO)


async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()

app = web.Application()
app.router.add_route('POST', WEBHOOK_PATH, SimpleRequestHandler(dispatcher=dp, bot=bot))

if __name__ == '__main__':
    setup_application(app, dp)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
