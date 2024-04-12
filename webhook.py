from flask import Flask, request
from bot import bot
from telegram import Update,Bot
bot.delete_webhook()
URL = "https://vercel.com/easys-projects/"
TOKEN = "6430079230:AAGxyL2dzCo2LJFSwuTxtmguVKv2fdlxLYw"
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    bot.process_update(update)
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    bot_instance = Bot(TOKEN)
    s = bot_instance.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
