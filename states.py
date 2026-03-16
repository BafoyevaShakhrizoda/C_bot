from aiogram.fsm.state import State, StatesGroup


class ApplicationForm(StatesGroup):
    full_name = State()
    phone = State()
    direction = State()
    technologies = State()
    portfolio = State()
    confirm = State()
