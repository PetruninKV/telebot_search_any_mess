from aiogram import Router
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message

from lexicon.lexicon import LEXICON

router: Router = Router()


@router.message(CommandStart())
async def processing_start_command(message: Message):
    await message.answer(text=LEXICON['/start'])


@router.message(Command(commands='about'))
async def processing_about_command(message: Message):
    await message.answer(text=LEXICON['/about'])


@router.message(Command(commands='rules'))
async def processing_rules_command(message: Message):
    await message.answer(text=LEXICON['/rules'])


@router.message(Command(commands='send_channels'))
async def processing_send_channels_command(message: Message):
    await message.answer(text=LEXICON['/send_channels'])


@router.message(Command(commands='send_words'))
async def processing_send_words_command(message: Message):
    await message.answer(text=LEXICON['/send_words'])


@router.message(Command(commands='help'))
async def processing_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])