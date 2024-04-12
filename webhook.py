from flask import Flask, request
from .bot import bot
URL = "vercel.com/easys-projects/"
TOKEN = "6430079230:AAGxyL2dzCo2LJFSwuTxtmguVKv2fdlxLYw"
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    setup().process_update(update)
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
