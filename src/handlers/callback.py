from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

from src.data.state.repeat_state import RepeatState
from src.lib.anonymouse import AnonyMouse

posts_cb = CallbackData('post', 'id', 'action')

def register_callback_handler(dp: Dispatcher, bot: Bot, anonymouse: AnonyMouse):
    @dp.callback_query_handler(posts_cb.filter(action=['send']))
    async def send_email(query: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        try:
            await anonymouse.send_email_message(data["mail"], data["title"], data["body"])
            await bot.send_message(query.message.chat.id, "message was sent")
        except KeyError as e:
            print(e)
        await state.finish()

    @dp.callback_query_handler(posts_cb.filter(action=["edit_title"]))
    async def edit_title(query: types.CallbackQuery):
        await RepeatState.repeat_title.set()
        await bot.send_message(query.message.chat.id, "send new title")

    @dp.callback_query_handler(posts_cb.filter(action=["edit_body"]))
    async def edit_body(query: types.CallbackQuery):
        await RepeatState.repeat_body.set()
        await bot.send_message(query.message.chat.id, "send new body")

    @dp.callback_query_handler(posts_cb.filter(action=["edit_mail"]))
    async def edit_mail(query: types.CallbackQuery, state: FSMContext):
        await RepeatState.repeat_mail.set()
        await bot.send_message(query.message.chat.id, "send new mail")
