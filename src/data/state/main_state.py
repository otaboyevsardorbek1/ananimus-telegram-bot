from aiogram.dispatcher.filters.state import State, StatesGroup


class MainStates(StatesGroup):
    send_mail: State = State()
    send_title: State = State()
    send_body: State = State()
