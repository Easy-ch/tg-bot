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
from utils import  Cost_Clothing,Orders_states,Course_states
from db import Course,Order
# Bot token can be obtained via https://t.me/BotFather


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
async def photo(message:types.Message):
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
            course = await Course.get_course()
            
            buy=float((message.text).replace(',',''))
            count=math.floor(buy*course+2500)
            await message.answer(f'  {count} ₽ - стоимость вашего заказа (с учетом комиссий)')
            await state.finish()
    except ValueError:
        await message.answer(messages['warning'])


@dp.message_handler(lambda c: c.text =='Одежда')
async def photo_clothes(message:types.Message):
    # await state.set_state(Cost_Clothing.choose_clothes)
    await Cost_Clothing.choose_clothes.set()
    photo = InputFile('gaid2.jpg')
    await bot.send_photo(chat_id=message.chat.id,photo=photo)
    await message.answer(messages['help'])


@dp.message_handler(state=Cost_Clothing.choose_clothes)
async def calculation_clothes(message:types.Message, state:FSMContext):
    try:
        if message.text.isdigit():  
            await state.update_data(buy=True)
            course = await Course.get_course()
            buy=float((message.text).replace(',',''))
            count=math.floor(buy*course+2500)-200
            await message.answer(f'  {count} ₽ - стоимость вашего заказа (с учетом комиссий)')
            await state.finish()
    except ValueError:
        await message.answer(messages['warning'])
        


@dp.message_handler(lambda c: c.text == 'Вернуться в главное меню',state='*')
async def main_menu(message:types.Message):
    await command_start_handler(message) 
    

@dp.message_handler(lambda msg: msg.text == 'Сменить курс',state='*')
async def course_change(message:types.Message):
    await message.answer(messages['course'])
    await Course_states.waiting_for_course_change.set()

@dp.message_handler(state=Course_states.waiting_for_course_change)
async def change(message:types.Message, state: FSMContext):
    if message.from_user.id == int(ADMIN_ID):
        try:
            await state.update_data(value=True)
            value = float(message.text.replace(',','.'))
            await Course.set_course(value)
            await message.answer(f'Новое значение курса: {value}')
            await state.finish()
        except ValueError:
            await message.answer('Неверный формат!')
    else:
        await message.answer('ахахах,засранец, как ты узнал? (нет тебя в админах)')

@dp.message_handler(lambda msg: msg.text == 'Текущий курс юаня',state='*')
async def course_info(message:types.Message):
    course = await Course.get_course()
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


@dp.message_handler(lambda msg:msg.text == 'Товар оригинал?',state='*')
async def faq_answer2(message:types.Message):
    await message.answer(messages['info2'])

@dp.message_handler(lambda msg: msg.text == 'Добавить заказ',state='*')
async def add_order_start(message:types.Message):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer('Введите номер заказа')
        await Orders_states.waiting_for_order_id.set()
    else:
        await message.answer('ахахах,засранец, как ты узнал? (нет тебя в админах)') 

@dp.message_handler(state=Orders_states.waiting_for_order_id)
async def process_order_id(message:types.Message,state:FSMContext):
    order_id = message.text
    await state.update_data(order_id = str(order_id))
    try:
        await message.answer('Введите описание заказа')
        await Orders_states.next()
    except ValueError:
        await message.answer('Неверный формат!')

@dp.message_handler(state=Orders_states.waiting_for_order_description)
async def process_order_description(message:types.Message,state:FSMContext):
    description = message.text
    await state.update_data(description=str(description))
    await message.answer('Введите статус заказа')
    await Orders_states.next()

@dp.message_handler(state=Orders_states.waiting_for_order_status)
async def process_order_status(message:types.Message,state:FSMContext):
    status = message.text
    await state.update_data(status = str(status))
    try:
        await message.answer('Введите пароль для доступа к заказу')
        await Orders_states.next()
    except ValueError:
        await message.answer('Неверный формат!')

@dp.message_handler(state=Orders_states.waiting_for_order_password)
async def process_order_password(message:types.Message,state: FSMContext):
    access_password = message.text.strip()
    await state.update_data(access_password=str(access_password))
    user_data = await state.get_data()
    await Order.add_order(user_data['order_id'],user_data['description'],user_data['status'],user_data['access_password'])
    await message.answer('Заказ успешно добавлен!')
    await state.finish()

@dp.message_handler(lambda msg: msg.text == 'Удалить заказ',state='*')
async def delete_order_start(message:types.Message):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer('Введите номер заказа,который нужно удалить')
        await Orders_states.waiting_for_order_delete.set()
    else:
        await message.answer('ахахах,засранец, как ты узнал? (нет тебя в админах)') 


@dp.message_handler(state=Orders_states.waiting_for_order_delete)
async def process_delete_order(message:types.Message,state:FSMContext):
    order_id = message.text
    order_exists = await Order.order_exists(order_id)
    if not order_exists:
        await message.answer('Заказ с таким номером не найден.')
        await state.finish()
        return
    
    await Order.remove_order(order_id)
    await message.answer('Заказ успешно удален')
    await state.finish()

@dp.message_handler(lambda msg: msg.text == 'Изменить статус', state='*')
async def process_change_status_start(message:types.Message):
    await message.answer('Введите номер заказа, в котором хотите поменять статус')
    await Orders_states.waiting_change_id.set()

@dp.message_handler(state=Orders_states.waiting_change_id)
async def process_change_status_id(message:types.Message,state:FSMContext):
    order_id = message.text.strip()
    await state.update_data(order_id=str(order_id))
    await message.answer('Введите новый статус для заказа')
    await Orders_states.next()

@dp.message_handler(state=Orders_states.waiting_change_status)
async def process_change_status_order(message:types.Message,state:FSMContext):
    new_status = message.text.strip()
    await state.update_data(status=str(new_status))
    user_data = await state.get_data()
    order_id = user_data.get('order_id')
    status = user_data.get('status')
    order = await Order.get_order(user_data['order_id'])
    if order:
        await Order.change_status_order(order_id,status)
        await message.answer('Статус заказа успешно изменен!')
    else:
        await message.answer('Заказ с таким номером не найден.')
    await state.finish()


@dp.message_handler(lambda msg: msg.text == 'Отследить заказ',state='*')
async def process_view_order(message:types.Message):
    await message.answer('Введите номер заказа')
    await Orders_states.waiting_order_view.set()

@dp.message_handler(state=Orders_states.waiting_order_view)
async def process_view_password(message:types.Message,state:FSMContext):
    order_id = message.text
    await state.update_data(order_id = str(order_id))
    await message.answer('Введите пароль')
    await Orders_states.next()


@dp.message_handler(state=Orders_states.waiting_view_password)
async def process_check_password(message:types.Message,state:FSMContext):
    access_password = message.text
    user_data = await state.get_data()
    order = await Order.get_order(user_data['order_id'])
    if order:
        if access_password == order['access_password']:
            description = order['description']
            status = order['status']
            await message.answer(f'Заказ {description},{status}')
            await state.finish
        else:
            await message.answer('Пароль неверный')
    else:
        await message.answer('Неверный номер заказа')   


@dp.message_handler()
async def valid(message:types.Message):
    await message.answer(messages['valid'])

async def echo_handler(message:types.Message) -> None:
        try:
            await message.copy_to(chat_id=message.chat.id)
        except TypeError:
            await message.answer("Nice try!")

