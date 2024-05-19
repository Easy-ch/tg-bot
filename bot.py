import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher,html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from keyboards import Keyboards
from messages import messages
from aiogram import types
from aiogram.types import FSInputFile
import math
import os
from dotenv import load_dotenv


load_dotenv()
# Bot token can be obtained via https://t.me/BotFather
TOKEN = str(os.getenv('TOKEN'))

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
course = 0

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    await deleteweb(bot)
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def command_start_handler(message:types.Message) -> None:
    await message.answer(messages['welcome_text'],reply_markup= Keyboards.start_keyboard())
    if message.from_user.id == int(os.getenv('ADMIN_ID')) :
        await message.answer('Вы зарегестрировались как админ',reply_markup=Keyboards.admin_keyboard())

@dp.message(lambda c: c.text == 'Рассчитать стоимость товара')
async def change_category(message:types.Message):
    await message.answer(messages['category'],reply_markup=Keyboards.keyboard_cost())

@dp.message(lambda c: c.text =='Обувь')
async def photo(message:types.Message):
    photo = FSInputFile('gaid.jpg')
    await bot.send_photo(chat_id=message.chat.id,photo=photo)
    await message.answer(messages['help'])

@dp.message(lambda c: c.text == 'Вернуться в главное меню')
async def main_menu(message:types.Message):
    await command_start_handler(message) 

@dp.message(lambda message: message.text.isdigit())
async def calculation(message:types.Message):
    try:
        global course
        buy=float((message.text).replace(',',''))
        count=math.floor(buy*course+1000)+1800
        await message.answer(f' от {count} ₽ - стоимость вашего заказа (с учетом комиссий)')
    except ValueError:
        await message.answer(messages['warning'])

@dp.message(lambda msg: msg.text == 'Сменить курс')
async def course_change(message:types.Message):
    await message.answer(messages['course'])
    
@dp.message(lambda message: 'Setcourse='in message.text)
async def change(message:types.Message):
    if message.from_user.id == int('5034422722'):
        global course
        value = message.text.split('=', 1)[1].strip()
        course = float(value.replace(',','.'))
        await message.answer(f'Новое значение курса: {course}')
    else:
        await message.answer('ахахах,засранец, как ты узнал? (нет тебя в админах)')
       
@dp.message(lambda msg: msg.text == 'Какой текущий курс юаня?')
async def course_info(message:types.Message):
    await message.answer(f'Текущий курс юаня {course} ₽')

@dp.message(lambda msg: msg.text == 'Сделать заказ')    
async def make_delivery(message:types.Message):
    await message.answer(messages['make_delivery'])
    video = FSInputFile('video_gaid.mp4')
    await bot.send_video(chat_id=message.chat.id,video=video)

@dp.message(lambda msg: msg.text == 'Написать отзыв')
async def feedback(message:types.Message):
    await message.answer(messages['feedback'])

@dp.message(lambda msg: msg.text == 'FAQ')
async def faq(message:types.Message):
    await message.answer('Здесь вы можете узнать ответы на часто задаваемые вопросы:',reply_markup=Keyboards.keyboard_Faq())

@dp.message(lambda msg: msg.text == 'Каковы сроки доставки?')
async def faq_answer(message:types.Message):
    await message.answer(messages['info'])

@dp.message()
async def valid(message:types.Message):
    await message.answer(messages['valid'])
    

async def echo_handler(message:types.Message) -> None:   
        try:
            await message.copy_to(chat_id=message.chat.id)
        except TypeError:
            await message.answer("Nice try!")

def register_handlers(dp: Dispatcher):
    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(change_category, lambda c: c.text == 'Рассчитать стоимость товара')
    dp.message.register(photo, lambda c: c.text == 'Обувь')
    dp.message.register(main_menu, lambda c: c.text == 'Вернуться в главное меню')
    dp.message.register(calculation, lambda message: message.text.isdigit())
    dp.message.register(course_change, lambda msg: msg.text == 'Сменить курс')
    dp.message.register(change, lambda message: 'Setcourse=' in message.text)
    dp.message.register(course_info, lambda msg: msg.text == 'Какой текущий курс юаня?')
    dp.message.register(make_delivery, lambda msg: msg.text == 'Сделать заказ')
    dp.message.register(feedback, lambda msg: msg.text == 'Написать отзыв')
    dp.message.register(faq, lambda msg: msg.text == 'FAQ')
    dp.message.register(faq_answer, lambda msg: msg.text == 'Каковы сроки доставки?')
    dp.message.register(valid)
