import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
import os
from dotenv import load_dotenv
from bot import register_handlers

load_dotenv()
TOKEN = os.getenv('TOKEN')
# webhook settings
WEBHOOK_HOST = 'https://bbbb-alpha.vercel.app/'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
bot = Bot(TOKEN)


logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчера с хранилищем состояний
dp = Dispatcher(storage=MemoryStorage())
register_handlers(dp)

async def on_startup():
    logging.info('Starting up...')
    await bot.set_webhook(WEBHOOK_URL)

    # Устанавливаем команды бота
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="help", description="Помощь")
        ],
        scope=BotCommandScopeDefault()
    )
    logging.info(f"Webhook URL: {WEBHOOK_URL}")

async def on_shutdown():
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    logging.warning('Bye!')

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

app = web.Application()
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app,path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)

if __name__ == '__main__':
    web.run_app(app)
