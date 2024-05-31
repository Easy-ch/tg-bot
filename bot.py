import asyncio
import logging
import os
import math
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile, ParseMode
from aiogram.dispatcher.filters import CommandStart
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import Keyboards
from messages import messages
from config import TOKEN,ADMIN_ID
# Bot token can be obtained via https://t.me/BotFather


bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
course = 0
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
dp.middleware.setup(LoggingMiddleware())
async def deleteweb(bot:Bot):
    await bot.delete_webhook()
async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    await deleteweb(bot)
    await dp.start_polling(bot)

@dp.message_handler(CommandStart())
async def command_start_handler(message:types.Message) -> None:
    await message.answer(messages['welcome_text'],reply_markup= Keyboards.start_keyboard())
    if message.from_user.id == int(ADMIN_ID) :
        await message.answer('Вы зарегестрировались как админ',reply_markup=Keyboards.admin_keyboard())

@dp.message_handler(lambda c: c.text == 'Рассчитать стоимость товара')
async def change_category(message:types.Message):
    await message.answer(messages['category'],reply_markup=Keyboards.keyboard_cost())

@dp.message_handler(lambda c: c.text =='Обувь')
async def photo(message:types.Message):
    photo = InputFile('gaid.jpg')
    await bot.send_photo(chat_id=message.chat.id,photo=photo)
    await message.answer(messages['help'])

@dp.message_handler(lambda c: c.text == 'Вернуться в главное меню')
async def main_menu(message:types.Message):
    await command_start_handler(message) 

@dp.message_handler(lambda message: message.text.isdigit())
async def calculation(message:types.Message):
    try:
        global course
        buy=float((message.text).replace(',',''))
        count=math.floor(buy*course+1000)+1800
        await message.answer(f' от {count} ₽ - стоимость вашего заказа (с учетом комиссий)')
    except ValueError:
        await message.answer(messages['warning'])

@dp.message_handler(lambda msg: msg.text == 'Сменить курс')
async def course_change(message:types.Message):
    await message.answer(messages['course'])

@dp.message_handler(lambda message: 'Setcourse='in message.text)
async def change(message:types.Message):
    if message.from_user.id == int(ADMIN_ID):
        global course
        value = message.text.split('=', 1)[1].strip()
        course = float(value.replace(',','.'))
        await message.answer(f'Новое значение курса: {course}')
    else:
        await message.answer('ахахах,засранец, как ты узнал? (нет тебя в админах)')

@dp.message_handler(lambda msg: msg.text == 'Какой текущий курс юаня?')
async def course_info(message:types.Message):
    await message.answer(f'Текущий курс юаня {course} ₽')

@dp.message_handler(lambda msg: msg.text == 'Сделать заказ')    
async def make_delivery(message:types.Message):
    await message.answer(messages['make_delivery'])
    video = InputFile('video_gaid.mp4')
    await bot.send_video(chat_id=message.chat.id,video=video)

@dp.message_handler(lambda msg: msg.text == 'Написать отзыв')
async def feedback(message:types.Message):
    await message.answer(messages['feedback'])

@dp.message_handler(lambda msg: msg.text == 'FAQ')
async def faq(message:types.Message):
    await message.answer('Здесь вы можете узнать ответы на часто задаваемые вопросы:',reply_markup=Keyboards.keyboard_Faq())

@dp.message_handler(lambda msg: msg.text == 'Каковы сроки доставки?')
async def faq_answer(message:types.Message):
    await message.answer(messages['info'])

@dp.message_handler()
async def valid(message:types.Message):
    await message.answer(messages['valid'])

async def echo_handler(message:types.Message) -> None:
        try:
            await message.copy_to(chat_id=message.chat.id)
        except TypeError:
            await message.answer("Nice try!")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start_handler, CommandStart())
    dp.register_message_handler(change_category, lambda c: c.text == 'Рассчитать стоимость товара')
    dp.register_message_handler(photo, lambda c: c.text == 'Обувь')
    dp.register_message_handler(main_menu, lambda c: c.text == 'Вернуться в главное меню')
    dp.register_message_handler(calculation, lambda message: message.text.isdigit())
    dp.register_message_handler(course_change, lambda msg: msg.text == 'Сменить курс')
    dp.register_message_handler(change, lambda message: 'Setcourse=' in message.text)
    dp.register_message_handler(course_info, lambda msg: msg.text == 'Какой текущий курс юаня?')
    dp.register_message_handler(make_delivery, lambda msg: msg.text == 'Сделать заказ')
    dp.register_message_handler(feedback, lambda msg: msg.text == 'Написать отзыв')
    dp.register_message_handler(faq, lambda msg: msg.text == 'FAQ')
    dp.register_message_handler(faq_answer, lambda msg: msg.text == 'Каковы сроки доставки?')
    dp.register_message_handler(valid)
