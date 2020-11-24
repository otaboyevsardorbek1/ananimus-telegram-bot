from aiogram.dispatcher.filters.state import StatesGroup, State


class RepeatState(StatesGroup):
    repeat_body: State = State()
    repeat_mail: State = State()
    repeat_title: State = State()
