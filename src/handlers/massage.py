from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.data.state.main_state import MainStates
from src.lib.button import Button


def register_message_handler(dp: Dispatcher, bot: Bot):
    button = Button()

    @dp.message_handler()
    async def process_start_command(message: types.Message) -> None:
        await MainStates.send_mail.set()
        await bot.send_message(message.chat.id, text="hello! Do you want to send an anonymous message? send mail")

    @dp.message_handler(state=MainStates.send_mail)
    async def accept_mail(message: types.Message, state: FSMContext):
        print("save")
        async with state.proxy() as data:
            data["mail"] = message.text
        await MainStates.send_title.set()
        await bot.send_message(message.chat.id, "send title message")

    @dp.message_handler(state=MainStates.send_title)
    async def accept_mail(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["title"] = message.text
        await MainStates.send_body.set()
        await bot.send_message(message.chat.id, "send body message")

    @dp.message_handler(state=MainStates.send_body)
    async def accept_mail(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["body"] = message.text
        return await message.answer(text="send message?",
                                    reply_markup=button.buttons(text=["yes", "edit title", "edit body", "edit mail"],
                                                                call_back=["send", "edit_title", "edit_body",
                                                                           "edit_mail"]
                                                                )
                                    )

    @dp.message_handler(state="repeat_mail")
    async def repeat_mail(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["mail"] = message.text
        await state.finish()
        return await message.answer(text="send message?",
                                    reply_markup=button.buttons(text=["yes", "edit title", "edit body", "edit mail"],
                                                                call_back=["send", "edit_title", "edit_body",
                                                                           "edit_mail"]
                                                                )
                                    )

    @dp.message_handler(state="repeat_title")
    async def repeat_mail(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["title"] = message.text
            await state.finish()
            return await message.answer(text="send message?",
                                        reply_markup=button.buttons(
                                            text=["yes", "edit title", "edit body", "edit mail"],
                                            call_back=["send", "edit_title", "edit_body",
                                                       "edit_mail"]
                                        )
                                        )

    @dp.message_handler(state="repeat_body")
    async def repeat_mail(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["body"] = message.text
            await state.finish()
            return await message.answer(text="send message?",
                                        reply_markup=button.buttons(
                                            text=["yes", "edit title", "edit body", "edit mail"],
                                            call_back=["send", "edit_title", "edit_body",
                                                       "edit_mail"]
                                        )
                                        )
