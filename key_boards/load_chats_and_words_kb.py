from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_KEYBOARDS



def create_load_data(button: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=LEXICON_KEYBOARDS[button] 
                                         if button in LEXICON_KEYBOARDS else button,
                                         callback_data=button))
    return kb_builder.as_markup()