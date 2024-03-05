from aiogram.dispatcher.filters.state import StatesGroup

class RepeatState(StatesGroup):
    REPEAT = State()



from aiogram.dispatcher.filters.state import StatesGroup, State

class RepeatState(StatesGroup):
    REPEAT_BODY = State()
    REPEAT_MAIL = State()
    REPEAT_TITLE = State()

