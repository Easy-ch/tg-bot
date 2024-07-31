from aiogram.dispatcher.filters.state import State, StatesGroup

class Cost_Clothing(StatesGroup):
    choose_shoes = State()
    choose_clothes = State()

class Orders_states(StatesGroup):
    waiting_for_order_id = State()
    waiting_for_order_description = State()
    waiting_for_order_status = State()
    waiting_for_order_photo = State()
    waiting_for_order_password = State()
    waiting_for_order_delete = State()
    waiting_order_view = State()
    waiting_view_password = State()
    waiting_change_id = State()
    waiting_change_status = State()

    
class Course_states(StatesGroup):
    waiting_for_course_change = State()