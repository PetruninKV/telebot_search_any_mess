from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_KEYBOARDS



def create_one_button_kb(button: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=LEXICON_KEYBOARDS[button] 
                                         if button in LEXICON_KEYBOARDS else button,
                                         callback_data=button))
    return kb_builder.as_markup()


def create_regular_keyboard(*buttons: str) -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    kb_builder.row(
        *[KeyboardButton(text=LEXICON_KEYBOARDS[button] if button in LEXICON_KEYBOARDS else button)
           for button in buttons ], width=2)
    return kb_builder.as_markup(resize_keyboard=True, selective=True)