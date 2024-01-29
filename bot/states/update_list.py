from aiogram.dispatcher.filters.state import StatesGroup, State


class UpdateList(StatesGroup):
    start = State()
    update = State()
