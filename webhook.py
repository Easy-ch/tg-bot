from flask import Flask, request
from bot import bot
from telegram import Update, Bot
from telebot import apihelper
URL = "https://bbbb-alpha.vercel.app/"
TOKEN = "6430079230:AAGxyL2dzCo2LJFSwuTxtmguVKv2fdlxLYw"

app = Flask(__name__)
apihelper.proxy = {'http':'https://88.204.154.155:8080'}
@app.route('/')
def index():
    return 'Hello World!'

@app.route('/'.format(TOKEN), methods=['POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    bot.process_update(update)
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
async def set_webhook():
    bot_instance = Bot(TOKEN)
    s = await bot_instance.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

# Добавляем маршрут для обработки POST запросов на /TOKEN
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.json, bot)
    bot.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
