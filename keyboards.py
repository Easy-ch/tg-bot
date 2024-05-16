from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class Keyboards:
    @staticmethod
    def admin_keyboard():
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Добавить заказ'), 
                    KeyboardButton(text='Сменить курс')
                ], 
                [
                    KeyboardButton(text='Вернуться в главное меню')
                ]
            ], 
            resize_keyboard=True,
            one_time_keyboard=False,
        )
        return keyboard

    @staticmethod
    def start_keyboard():
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Рассчитать стоимость товара'), 
                    KeyboardButton(text='Какой текущий курс юаня?'),
                ],
                [
                    KeyboardButton(text='FAQ'), 
                    KeyboardButton(text='Сделать заказ'), 
                    KeyboardButton(text='Написать отзыв')
                ]
            ], 
            resize_keyboard=True
        )
        return keyboard 

    @staticmethod
    def keyboard_cost():
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Обувь'), 
                    KeyboardButton(text='Вернуться в главное меню')
                ]
            ], 
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def keyboard_Faq():
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Каковы сроки доставки?'), 
                    KeyboardButton(text='Вернуться в главное меню')
                ]
            ], 
            resize_keyboard=True
        )
        return keyboard 