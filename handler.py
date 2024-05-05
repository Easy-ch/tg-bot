import telebot
from keyboards import KeyBoards
token='6430079230:AAGxyL2dzCo2LJFSwuTxtmguVKv2fdlxLYw'
bot=telebot.TeleBot(token)
course = 0
import math

@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_text = 'Здравствуйте, это Telegram-бот магазина WN market, здесь вы сможете отследить свой заказ, рассчитать стоимость заказа, узнать ответы на самые часто задаваемые вопросы и многое другое! '
    bot.send_message(message.chat.id,welcome_text,reply_markup=KeyBoards.start_keyboard())

@bot.message_handler(func=lambda message: message.text == 'FAQ')
def handler_faq(message):
    bot.send_message(message.chat.id,'Здесь вы можете узнать ответы на часто задаваемые вопросы:',reply_markup=KeyBoards.keyboard_Faq())

@bot.message_handler(func=lambda message: message.text == 'Каковы сроки доставки?')
def handler_dost(message):
    bot.send_message(message.chat.id,"""❗️Расскажем про нашу доставку
После полной предоплаты заказа, ваш товар отправляют из Китая в Москву (в среднем занимает от 17 до 25 дней), потом СДЭКом до вашего города получения (в среднем 2-7 дней).

В среднем доставка занимает от 16 до 40 дней!""")
    
@bot.message_handler(func=lambda message: message.text == 'Вернуться в главное меню')
def main_menu(message):
    handle_start(message)

@bot.message_handler(commands=['admin'])
def handler_admin(message):
   bot.send_message(message.chat.id,'Привет админ, выбери действие',reply_markup=KeyBoards.admin_keyboard())
def handler_auth(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    allowed_user_id = ['5034422722','935176577']
    admin_password = 'Wn_90090'
    if user_id  in allowed_user_id:
        bot.send_message(chat_id, "Привет, админ. ")
    else:
        bot.send_message(chat_id,'Для доступа в панель администрации введите пароль..')
        bot.register_next_step_handler(message,password_check,admin_password)
def password_check(message,admin_password):
    chat_id = message.chat.id
    password_attempt = message.text.strip()
    if password_attempt == admin_password:
        bot.send_message(chat_id, "Привет, админ. ")
        bot.send_message(message.chat.id,'Выберите действие')
    else:
        bot.send_message(chat_id,"Пароль неверный!")

@bot.message_handler(func=lambda message: message.text =='Сменить курс')
def change(message):
    cur=bot.send_message(message.chat.id, "Введите новое значение курса: ")
    bot.register_next_step_handler(cur,ans)
def ans(message):
    global course
    course = float((message.text).replace(',',''))
    bot.send_message(message.chat.id, f'Новое значение курса: {course}')

@bot.message_handler(func=lambda message: message.text =='Какой текущий курс юаня?')
def now_course(message):
    bot.send_message(message.chat.id,f'Текущий курс юаня {course} ₽')

@bot.message_handler(func=lambda message: message.text =='Рассчитать стоимость товара')
def change_category(message):
   bot.send_message(message.chat.id,"Выберите категорию товара",reply_markup=KeyBoards.keyboard_cost())
@bot.message_handler(func=lambda message: message.text =='Обувь' )
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
        bot.send_message(message.chat.id,'Напишите сумму заказа!')

@bot.message_handler(func=lambda message: message.text =='Сделать заказ')
def make_delivery(message):
    video_gaid = open('video_gaid.mp4','rb')
    bot.send_video(message.chat.id,video_gaid)
    bot.send_message(message.chat.id,""" Сделать заказ
Заказ можно оформить через телеграм-аккаунт Прием заказов wnmarket.
Для того, чтобы оформить заказ нужно отправить артикул товара и необходимый размер, также можно фотографию товара (инструкция о том, где можно найти артикул Poizon прикрепляем в видео 📌)
 @wnmarket1
  """)
@bot.message_handler(func=lambda message: message.text =='Написать отзыв')
def feedback(message):
    text = """ Написать отзыв:

Написать свой отзыв вы сможете по ссылке ниже, просто напишите сообщение на этот аккаунт со своим мнением о работе сервиса и мы обязательно его выложим в наш канал с отзывами - https://t.me/wnmarketfeedback
"""
    bot.send_message(message.chat.id,text)   
