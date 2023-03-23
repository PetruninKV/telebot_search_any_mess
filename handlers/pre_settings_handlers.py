from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message, CallbackQuery

#FSM
from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
# from aiogram.fsm.storage.memory import MemoryStorage


from lexicon.lexicon import LEXICON, LEXICON_CALLBACK
from database.database import user_dict_template, users_db
from key_boards.any_keyboards import create_one_button_kb
from filters.filters_for_load_data import IsListChannels, IsListKeywords


class FSMGetData(StatesGroup):
    get_channels = State()
    get_keywords = State()

231
router: Router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def processing_start_command(message: Message):
    await message.answer(text=LEXICON['/start'])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
        print(users_db)


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def processing_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы вне заполнения бд')


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def processing_cancel_command(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из заполнения бд. Данные не сохранились.')
    await state.clear()


@router.message(Command(commands='about'), StateFilter(default_state))
async def processing_about_command(message: Message):
    await message.answer(text=LEXICON['/about'])


@router.message(Command(commands='rules'), StateFilter(default_state))
async def processing_rules_command(message: Message):
    await message.answer(text=LEXICON['/rules'])


@router.message(Command(commands='pre_start'), StateFilter(default_state))
async def processing_prestart_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/pre_start'], reply_markup=create_one_button_kb('load_channels'))
    

@router.callback_query(Text(text='load_channels'), StateFilter(default_state))
async def load_channels_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_CALLBACK['load_channels'])
    await state.set_state(FSMGetData.get_channels)


@router.message(StateFilter(FSMGetData.get_channels), F.text, IsListChannels())
async def processing_channels_sent(message: Message, state: FSMContext, channels: list[dict]):
    # text = ("\n".join(channel for channel in channels))
    await message.answer(text='корректно')
    await state.update_data(list_channels=channels)
    await message.answer(text=LEXICON['succes_load_channels'], reply_markup=create_one_button_kb('load_keywords'))
    

@router.message(StateFilter(FSMGetData.get_channels))
async def processing_channels_sent(message: Message, state: FSMContext):
    await message.answer(text='не корректно')
    
    
@router.callback_query(Text(text='load_keywords'), StateFilter(FSMGetData.get_channels)) 
async def load_keywords_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_CALLBACK['load_keywords'])
    await state.set_state(FSMGetData.get_keywords)


@router.message(StateFilter(FSMGetData.get_keywords), F.text, IsListKeywords() ) # написать фильтр для проверки списка состоящего ключевых слов
async def processing_keywords_sent(message: Message, state: FSMContext, keywords: list[dict]):
    await message.answer(text='корректно')
    await state.update_data(list_keywords=keywords)
    await message.answer(text=LEXICON['succes_load_keywords'])
    users_db[message.from_user.id] = await state.get_data()
    await state.clear()
    await message.answer(text=LEXICON['check_lists'])



@router.message(StateFilter(FSMGetData.get_keywords))
async def processing_channels_sent(message: Message, state: FSMContext):
    await message.answer(text='не корректно')


@router.message(Command(commands='look'))
async def procassing_look_command(message: Message):
    list_channels = users_db[message.from_user.id]['list_channels']
    list_keywords = users_db[message.from_user.id]['list_keywords']
    await message.answer(text=list_channels)
    await message.answer(text=list_keywords)
    await message.answer(text=LEXICON['/look'])
    


@router.message(Command(commands='help'))
async def processing_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])