from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.data.state.main_state import MainStates
from src.lib.button import Button

def register_handlers(dp: Dispatcher, bot: Bot):
    button = Button()

    @dp.message_handler(state="*")
    async def process_unknown_message(message: types.Message, state: FSMContext):
        await state.finish()
        await message.reply("Unknown message. Please start over.")

    @dp.message_handler(commands=["start"])
    async def process_start_command(message: types.Message) -> None:
        await MainStates.send_mail.set()
        await bot.send_message(message.chat.id, text="hello! Do you want to send an anonymous message? send mail")

    async def ask_for_input(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data[message.state_group] = message.text
        await message.answer(text="send message?",
                             reply_markup=button.buttons(text=["yes", "edit title", "edit body", "edit mail"],
                                                         call_back=["send", "edit_title", "edit_body",
                                                                    "edit_mail"]
                                                         )
                             )

    @dp.message_handler(state=MainStates.send_mail, regexp="(mail|send mail)")
    async def accept_mail(message: types.Message, state: FSMContext):
        try:
            await ask_for_input(message, state)
        except Exception as e:
            await message.answer(text="Error initializing state: {}".format(e))

    @dp.message_handler(state=MainStates.send_title, regexp="(title|send title)")
    async def accept_title(message: types.Message, state: FSMContext):
        try:
            await ask_for_input(message, state)
        except Exception as e:
            await message.answer(text="Error initializing state: {}".format(e))

    @dp.message_handler(state=MainStates.send_body, regexp="(body|send body)")
    async def accept_body(message: types.Message, state: FSMContext):
        try:
            await ask_for_input(message, state)
        except Exception as e:
            await message.answer(text="Error initializing state: {}".format(e))

    @dp.message_handler(state="repeat_*", regexp="^(yes|edit .+)$")
    async def repeat_input(message: types.Message, state: FSMContext):
        state_proxy = await state.proxy()
        state_name = message.state.split("_")[1]
        state_proxy[state_name] = message.text
        await message.answer(text="send message?",
                             reply_markup=button.buttons(text=["yes", "edit title", "edit body", "edit mail"],
                                                         call_back=["send", "edit_title", "edit_body",
                                                                    "edit_mail"]
                                                         )
                             )
