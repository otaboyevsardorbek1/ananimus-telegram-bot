from aiogram.dispatcher.filters.state import State, StatesGroup

class MainStates(StatesGroup):
    mail_details = StateGroup(
        send_mail=State(),
        send_title=State(),
        send_body=State()
    )
