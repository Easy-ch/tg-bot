from telebot import TeleBot

bot = TeleBot('6722734578:AAE0e9osDxTybDKd4qovXXneqrSe9eES6ug', threaded=False)


@bot.message_handler()
def main(msg):
    bot.send_message(msg.chat.id, msg.text)
