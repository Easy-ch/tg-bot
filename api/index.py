from flask import Flask, request
from aiogram import types,Bot,Dispatcher
from bot import dp, bot,register_handlers
from dotenv import load_dotenv
import os
import requests
import asyncio
load_dotenv()
register_handlers(dp)
app = Flask(__name__)
TOKEN = os.getenv('TOKEN')
WEBHOOK_HOST = 'https://bbbb-alpha.vercel.app/'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# @app.on_event("startup")
# async def on_startup():
#     webhook_info = await bot.get_webhook_info()
#     if webhook_info.url != WEBHOOK_URL:


# @app.post(WEBHOOK_PATH)
# async def bot_webhook(request: Request):
#     telegram_update = types.Update(await request.json())
#     Dispatcher.set_current(dp)
#     Bot.set_current(bot)
#     await dp.process_update(telegram_update)
@app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    update = request.get_json()
    if not update:
        return 'ПУСТОЙ!!!!!!!!!!!!', 404
    # await dp.process_update(types.Update(**update))
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(types.Update(**update))
    return 'OK', 200
# @app.on_event("shutdown")
# async def on_shutdown():
#     await bot.session.close(
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
        print("Webhook set successfully!")
    else:
        print("Webhook was already set")

async def on_shutdown():
    await bot.session.close()



@app.get("/")
async def root():
    return {"message": "Bot webhook is running"}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_startup())
    response = requests.get(f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}')
    if response.status_code == 200:
        print("Webhook set successfully!")
    else:
        print("Failed to set webhook")
    app.run(host='0.0.0.0',port = 80,debug=True)


