from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

from src.data.state.repeat_state import RepeatState
from src.lib.anonymouse import AnonyMouse


def register_callback_handler(dp: Dispatcher, bot: Bot, anonymouse: AnonyMouse):
    posts_cb: CallbackData = CallbackData('post', 'id', 'action')

    @dp.callback_query_handler(posts_cb.filter(action=['send']))
    async def send(query: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            try:
                await anonymouse.send_email_message(data["mail"], data["title"], data["body"])
                await bot.send_message(query.message.chat.id, "message was sent")
            except KeyError as e:
                print(e)
        await state.finish()

    @dp.callback_query_handler(posts_cb.filter(action=["edit_title"]))
    async def send(query: types.CallbackQuery):
        await RepeatState.repeat_title.set()
        await bot.send_message(query.message.chat.id, "send new title")

    @dp.callback_query_handler(posts_cb.filter(action=["edit_body"]))
    async def send(query: types.CallbackQuery):
        await RepeatState.repeat_title.set()
        await bot.send_message(query.message.chat.id, "send new body")

    @dp.callback_query_handler(posts_cb.filter(action=["edit_mail"]))
    async def send(query: types.CallbackQuery, state: FSMContext):
        await RepeatState.repeat_title.set()
        await bot.send_message(query.message.chat.id, "send new mail")
