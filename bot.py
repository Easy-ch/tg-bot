# from db import get_course,set_course
import math
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile, ParseMode
from aiogram.dispatcher.filters import CommandStart
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import Keyboards
from messages import messages
from config import TOKEN,ADMIN_ID
from aiogram.dispatcher import FSMContext
from utils import  Cost_Clothing

# Bot token can be obtained via https://t.me/BotFather

course = 0
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
dp.middleware.setup(LoggingMiddleware())

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    await dp.start_polling(bot)
    

@dp.message_handler(CommandStart(),state='*')
async def command_start_handler(message:types.Message) -> None:

    await message.answer(messages['welcome_text'],reply_markup= Keyboards.start_keyboard())
    if message.from_user.id == int(ADMIN_ID) :
        await message.answer('Вы зарегестрировались как админ',reply_markup=Keyboards.admin_keyboard())

@dp.message_handler(lambda c: c.text == 'Рассчитать стоимость товара',state='*')
async def change_category(message:types.Message):
    await message.answer(messages['category'],reply_markup=Keyboards.keyboard_cost())

@dp.message_handler(lambda c: c.text =='Обувь',state='*')
async def photo(message:types.Message, state: FSMContext):
    # await state.set_state(Cost_Clothing.choose_shoes)
    await Cost_Clothing.choose_shoes.set()
    photo = InputFile('gaid.jpg')
    await bot.send_photo(chat_id=message.chat.id,photo=photo)
    await message.answer(messages['help'])

@dp.message_handler(state=Cost_Clothing.choose_shoes)
async def calculation_shoes(message:types.Message,state: FSMContext):
    try:  
        if message.text.isdigit():  
            await state.update_data(buy=True)
            # course = await get_course()
            global course
            buy=float((message.text).replace(',',''))
            count=math.floor(buy*course+2500)
            await message.answer(f'  {count} ₽ - стоимость вашего заказа (с учетом комиссий)')
            await state.finish()
    except ValueError:
        await message.answer(messages['warning'])


@dp.message_handler(lambda c: c.text =='Одежда')
async def photo_clothes(message:types.Message, state: FSMContext):
    # await state.set_state(Cost_Clothing.choose_clothes)
    await Cost_Clothing.choose_clothes.set()
    photo = InputFile('gaid.jpg')
    await bot.send_photo(chat_id=message.chat.id,photo=photo)
    await message.answer(messages['help'])


@dp.message_handler(state=Cost_Clothing.choose_clothes)
async def calculation_clothes(message:types.Message, state:FSMContext):
    await state.update_data(buy=True)
    try:
        if message.text.isdigit():  
            await state.update_data(buy=True)
           
            # course = await get_course()
            global course
            buy=float((message.text).replace(',',''))
            count=math.floor(buy*course+2500)-200
            await message.answer(f'  {count} ₽ - стоимость вашего заказа (с учетом комиссий)')
            await state.finish()
    except ValueError:
        await message.answer(messages['warning'])
        


@dp.message_handler(lambda c: c.text == 'Вернуться в главное меню',state='*')
async def main_menu(message:types.Message,state:FSMContext):
    await command_start_handler(message) 
    

@dp.message_handler(lambda msg: msg.text == 'Сменить курс',state='*')
async def course_change(message:types.Message):
    await message.answer(messages['course'])

@dp.message_handler(lambda message: 'Setcourse='in message.text,state='*')
async def change(message:types.Message):
    if message.from_user.id == int(ADMIN_ID):
        try:
            value = message.text.split('=', 1)[1].strip()
            value = float(value.replace(',','.'))
            # await set_course(value)
            global course
            await message.answer(f'Новое значение курса: {value}')
        except ValueError:
            await message.answer('Неверный формат!')
    else:
        await message.answer('ахахах,засранец, как ты узнал? (нет тебя в админах)')

@dp.message_handler(lambda msg: msg.text == 'Какой текущий курс юаня?',state='*')
async def course_info(message:types.Message):
    global course
    # course = await get_course()
    course = float('{:.2f}'.format(course))
    if course is not None:
        await message.answer(f'Текущий курс юаня {course} ₽')
    else: 
        await message.answer('Похоже, что курс еще не установлен...')

@dp.message_handler(lambda msg: msg.text == 'Сделать заказ',state='*')    
async def make_delivery(message:types.Message):
    await message.answer(messages['make_delivery'])
    video = InputFile('video_gaid.mp4')
    await bot.send_video(chat_id=message.chat.id,video=video)

@dp.message_handler(lambda msg: msg.text == 'Написать отзыв',state='*')
async def feedback(message:types.Message):
    await message.answer(messages['feedback'])

@dp.message_handler(lambda msg: msg.text == 'FAQ')
async def faq(message:types.Message):
    await message.answer('Здесь вы можете узнать ответы на часто задаваемые вопросы:',reply_markup=Keyboards.keyboard_Faq())

@dp.message_handler(lambda msg: msg.text == 'Каковы сроки доставки?',state='*')
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
    dp.register_message_handler(calculation_shoes, lambda message: message.text.isdigit())
    dp.register_message_handler(course_change, lambda msg: msg.text == 'Сменить курс')
    dp.register_message_handler(change, lambda message: 'Setcourse=' in message.text)
    dp.register_message_handler(course_info, lambda msg: msg.text == 'Какой текущий курс юаня?')
    dp.register_message_handler(make_delivery, lambda msg: msg.text == 'Сделать заказ')
    dp.register_message_handler(feedback, lambda msg: msg.text == 'Написать отзыв')
    dp.register_message_handler(faq, lambda msg: msg.text == 'FAQ')
    dp.register_message_handler(faq_answer, lambda msg: msg.text == 'Каковы сроки доставки?')
    dp.register_message_handler(calculation_clothes, lambda msg:msg.text.isdigit())
    dp.register_message_handler(photo, lambda c: c.text == 'Одежда')
    dp.register_message_handler(valid)
