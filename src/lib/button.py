from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class Button:

    def __init__(self):
        self.posts_cb: CallbackData = CallbackData('post', 'id', 'action')

    def button_all(self, text_button: str, callback: str) -> InlineKeyboardMarkup:
        """
        :param text_button:
        :param callback:
        :return:
        """
        inline_btn = InlineKeyboardButton(text=text_button,
                                          callback_data=self.posts_cb.new(id=callback, action=text_button), row_width=3)
        inline_kb = InlineKeyboardMarkup().add(inline_btn)
        return inline_kb

    def buttons(self, text: List[str], call_back: List[str]) -> InlineKeyboardMarkup:
        """
        :param text:
        :param call_back:
        :return:
        """
        inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
        for val, i in enumerate(text):
            inb = InlineKeyboardButton(text=i,
                                       callback_data=self.posts_cb.new(id=hash(call_back[val]),
                                                                       action=call_back[val]), )
            inline_kb.insert(inb)
        return inline_kb
