import telebot
import math
course = 0
token='6430079230:AAEDudbAk8MZfHUKhILZGv6i0TfKZd_EFXs'
bot=telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = 'Здравствуйте, это Telegram-бот магазина WN market, здесь вы сможете отследить свой заказ, рассчитать стоимость заказа, узнать ответы на самые часто задаваемые вопросы и многое другое! '
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
    button1 = telebot.types.KeyboardButton('Рассчитать стоимость товара')
    button2 = telebot.types.KeyboardButton('FAQ')
    button3 = telebot.types.KeyboardButton('Какой текущий курс юаня?')
    button4 = telebot.types.KeyboardButton('Сделать заказ')
    button = telebot.types.KeyboardButton('Написать отзыв')
    keyboard.add(button1,button2,button3,button4,button)
    bot.send_message(message.chat.id,welcome_text,reply_markup=keyboard)
def calculation(message):
    gaid=open('gaid.jpg','rb')
    bot.send_photo(message.chat.id,gaid)
    r=bot.send_message(message.chat.id,'Напишите сумму заказа в юанях')
    bot.register_next_step_handler(r,answer)

def answer(message):
    try:
     buy=float((message.text).replace(',',''))
     count=math.floor(buy*course+1000)+1800
     bot.send_message(message.chat.id,f' от {count} ₽ - стоимость вашего заказа (с учетом комиссий)')
    except ValueError:
       bot.send_message(message.chat.id,'Не нажимайте слишком часто!')

def curse(message):
   bot.send_message(message.chat.id,f'Текущий курс юаня = {course}₽ ')


@bot.message_handler(commands=['admin'])
def handle_admin(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    allowed_user_id = ['5034422722','935176577']
    admin_password = 'Wn_90090'
    if user_id  in allowed_user_id:
        bot.send_message(chat_id, "Привет, админ. ")
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
        button = telebot.types.KeyboardButton('Добавить заказ')
        btn = telebot.types.KeyboardButton('Сменить курс')
        button3 = telebot.types.KeyboardButton('Вернуться в главное меню')
        keyboard.add(button,btn,button3)
        bot.send_message(message.chat.id,'Выберите действие',reply_markup=keyboard)
    else:
       bot.send_message(chat_id,'Для доступа в панель администрации введите пароль..')
       bot.register_next_step_handler(message,password_check,admin_password)
def password_check(message,admin_password):
    chat_id = message.chat.id
    password_attempt = message.text.strip()
    if password_attempt == admin_password:
        bot.send_message(chat_id, "Привет, админ. ")
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
        button = telebot.types.KeyboardButton('Добавить заказ')
        btn = telebot.types.KeyboardButton('Сменить курс')
        button3 = telebot.types.KeyboardButton('Вернуться в главное меню')
        keyboard.add(button,btn,button3)
        bot.send_message(message.chat.id,'Выберите действие',reply_markup=keyboard)
    else:
        bot.send_message(chat_id,"Пароль неверный!")


def course_change(message):
    cur=bot.send_message(message.chat.id, "Введите новое значение курса: ")
    bot.register_next_step_handler(cur,ans)
def ans(message):
    global course
    course = float((message.text).replace(',',''))
    bot.send_message(message.chat.id, f'Новое значение курса: {course}'  )

def dost(message):
    bot.send_message(message.chat.id,"""❗️Расскажем про нашу доставку
После полной предоплаты заказа, ваш товар отправляют из Китая в Москву (в среднем занимает от 17 до 25 дней), потом СДЭКом до вашего города получения (в среднем 2-7 дней).

В среднем доставка занимает от 16 до 40 дней!""")
    
def buy(message):
    video_gaid = open('gaid_video.mp4','rb')
    bot.send_video(message.chat.id,video_gaid)
    bot.send_message(message.chat.id,""" Сделать заказ

Заказ можно оформить через телеграм-аккаунт Прием заказов wnmarket.

Для того, чтобы оформить заказ нужно отправить артикул товара и необходимый размер, также можно фотографию товара (инструкция о том, где можно найти артикул Poizon прикрепляем в видео 📌)
 @wnmarket1
  """)
    
def feedback (message):
   text = """ Написать отзыв:

Написать свой отзыв вы сможете по ссылке ниже, просто напишите сообщение на этот аккаунт со своим мнением о работе сервиса и мы обязательно его выложим в наш канал с отзывами - https://t.me/wnmarketfeedback
"""
   bot.send_message(message.chat.id,text)


  

@bot.message_handler(content_types=['text'])
def user(message):
    if message.text == 'Какой текущий курс юаня?':
        curse(message)
    elif message.text == 'Сделать заказ':
       buy(message)
    elif message.text=='Написать отзыв':
        feedback(message)
    elif message.text =='Рассчитать стоимость товара':
        keyboard5 = telebot.types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
        button = telebot.types.KeyboardButton('Обувь')
        but = telebot.types.KeyboardButton('Одежда')
        button2 = telebot.types.KeyboardButton('Техника')
        button3 = telebot.types.KeyboardButton('Вернуться в главное меню')
        keyboard5.add(button,but,button2,button3)
        bot.send_message(message.chat.id,'Выберите категорию товара.',reply_markup=keyboard5)
    elif message.text =='Обувь':
        calculation(message)
    elif message.text =='Одежда':
        calculation(message)
    elif message.text =='Техника':
       calculation(message)
    elif message.text=='Вернуться в главное меню':
       send_welcome(message)
    elif message.text=='FAQ':
       keyboard2 = telebot.types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
       button4 = telebot.types.KeyboardButton('Каковы сроки доставки?')
       button6 = telebot.types.KeyboardButton('Вернуться в главное меню')
       keyboard2.add(button4,button6)
       bot.send_message(message.chat.id,'Здесь вы можете узнать ответы на часто задаваемые вопросы:',reply_markup=keyboard2)
    elif message.text=='Каковы сроки доставки?':
       dost(message)
    elif message.text=='Вернуться в главное меню':
       send_welcome(message)
    elif message.text == 'Сменить курс':
        course_change(message)
