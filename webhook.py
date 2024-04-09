from bot import bot
from fastapi import FastAPI

# Инициализация FastAPI приложения
app = FastAPI()

# Устанавливаем вебхук для обработки входящих сообщений
WEBHOOK_URL_PATH = "/bbbb"
WEBHOOK_URL_BASE = f"https://vercel.com/easys-projects/{WEBHOOK_URL_PATH}"
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE)

# Обработчик вебхука для FastAPI
@app.post(WEBHOOK_URL_PATH)
async def handle_webhook(request: Request):
    """
    Обработчик вебхука для FastAPI.
    """
    update = await request.json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return {"ok": True}
