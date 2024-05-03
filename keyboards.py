from telebot import types
class KeyBoards:
    @staticmethod
    def admin_keyboard():
        keyboard = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
        keyboard.add('Добавить заказ','Сменить курс','Вернуться в главное меню')
        return keyboard
    @staticmethod
    def start_keyboard():
        keyboard =types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
        keyboard.add('Рассчитать стоимость товара','FAQ','Какой текущий курс юаня?','Сделать заказ','Написать отзыв')
        return keyboard 
    @staticmethod
    def keyboard_cost():
        keyboard =types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
        keyboard.add('Обувь','Вернуться в главное меню')
        # ,'Одежда','Техника',
        return keyboard
    @staticmethod
    def keyboard_Faq():
        keyboard =types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=False)
        keyboard.add('Каковы сроки доставки?','Вернуться в главное меню')
        return keyboard 