from aiogram.dispatcher.filters.state import StatesGroup, State


class GroupState(StatesGroup):
    advertising_link = State()
    advertising_inline = State()
