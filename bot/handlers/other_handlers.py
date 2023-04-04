from aiogram import Router

from aiogram.types import Message

from lexicon.lexicon import LEXICON


router: Router = Router()


@router.message()
async def processing_other_messages(message: Message):
    await message.answer(text=LEXICON['other_messages'])