import telebot
from flask import Flask, request
import os
# Инициализация бота
token = '6430079230:AAGxyL2dzCo2LJFSwuTxtmguVKv2fdlxLYw'
bot = telebot.TeleBot(token)

# Создание Flask-приложения
app = Flask(__name__)

# Установка вебхука
@app.route('/webhook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return '', 200

# Обработчики команд и сообщений
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, это бот!')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Удаление вебхука
@app.route('/remove_webhook', methods=['GET'])
def remove_webhook():
    bot.remove_webhook()
    return 'Webhook removed', 200

# Установка вебхука
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    bot.set_webhook(url='https://bbbb-alpha.vercel.app/webhook')
    return 'Webhook set', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
