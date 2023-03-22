from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message, CallbackQuery

#FSM
from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage


from lexicon.lexicon import LEXICON, LEXICON_CALLBACK
from database.database import user_dict_template, users_db
from key_boards.load_chats_and_words_kb import create_load_data


class FSMGetData(StatesGroup):
    get_channels = State()
    get_keywords = State()



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
    await message.answer(text=LEXICON['/pre_start'], reply_markup=create_load_data('load_channels'))
    

@router.callback_query(Text(text='load_channels'), StateFilter(default_state))
async def load_channels_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_CALLBACK['load_channels'])
    await state.set_state(FSMGetData.get_channels)


@router.message(StateFilter(FSMGetData.get_channels), F.text.isalpha()) # написать фильтр для проверки списка состоящего из ссылок
async def processing_channels_sent(message: Message, state: FSMContext):
    await message.answer(text='корректно')
    await state.update_data(list_chats=message.text)
    await message.answer(text=LEXICON['succes_load_channels'], reply_markup=create_load_data('load_keywords'))
    

@router.message(StateFilter(FSMGetData.get_channels))
async def processing_channels_sent(message: Message, state: FSMContext):
    await message.answer(text='не корректно')
    
    
@router.callback_query(Text(text='load_keywords'), StateFilter(FSMGetData.get_channels)) 
async def load_keywords_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_CALLBACK['load_keywords'])
    await state.set_state(FSMGetData.get_keywords)


@router.message(StateFilter(FSMGetData.get_keywords), F.text.isdigit()) # написать фильтр для проверки списка состоящего ключевых слов
async def processing_keywords_sent(message: Message, state: FSMContext):
    await message.answer(text='корректно')
    await state.update_data(list_keywords=message.text)
    await message.answer(text=LEXICON['succes_load_keywords'])
    users_db[message.from_user.id] = await state.get_data()
    await state.clear()
    await message.answer(text='чтобы посмотреть списки выполните команду /look')
    print(users_db[message.from_user.id])


@router.message(StateFilter(FSMGetData.get_keywords))
async def processing_channels_sent(message: Message, state: FSMContext):
    await message.answer(text='не корректно')





# @router.message(Command(commands='send_channels'))
# async def processing_send_channels_command(message: Message):
#     await message.answer(text=LEXICON['/send_channels'])


# @router.message(Command(commands='send_words'))
# async def processing_send_words_command(message: Message):
#     await message.answer(text=LEXICON['/send_words'])


@router.message(Command(commands='help'))
async def processing_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])