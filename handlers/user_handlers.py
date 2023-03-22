from copy import deepcopy

from aiogram import Router
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from database.database import user_dict_template, users_db

router: Router = Router()


@router.message(CommandStart())
async def processing_start_command(message: Message):
    await message.answer(text=LEXICON['/start'])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
        print(users_db)


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