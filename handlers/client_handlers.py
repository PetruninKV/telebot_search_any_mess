from aiogram import Router

from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

#FSM
from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon import LEXICON, LEXICON_KEYBOARDS
from database.database import users_db
from key_boards.any_keyboards import create_one_button_kb, create_regular_keyboard


class FSMClientWork(StatesGroup):
    setting_work = State()
    work_on = State()



router: Router = Router()




@router.message(Command(commands='look'), StateFilter(default_state))
async def processing_look_command(message: Message):
    strk_channels = '\n'.join(users_db[message.from_user.id]['list_channels'])
    strk_keywords = '\n'.join(users_db[message.from_user.id]['list_keywords'])
    await message.answer(text=f"Будут отслуживаться чаты:\n<pre>{strk_channels}</pre>") #
    await message.answer(text=f"По наличию в сообщениях ключевых слов:\n<pre>{strk_keywords}</pre>")
    await message.answer(text=LEXICON['/look'], reply_markup=create_one_button_kb('work_on'))


@router.callback_query(Text(text='work_on'), StateFilter(default_state))
async def work_on_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Пользуйтесь кнопками для управления пересылкой сообщений. '
                                       'Никакие другие команды во время работы не воспринимаются', 
                                     reply_markup=create_regular_keyboard('go_forward_messages',
                                                                           'stop_forward_messages',
                                                                           'Выйти'))
    await state.set_state(FSMClientWork.setting_work)



@router.message(Text(text=LEXICON_KEYBOARDS['go_forward_messages']), StateFilter(FSMClientWork.setting_work))
async def processing_go_forward(message: Message, state: FSMContext):
    print('processing_go_forward')
    await state.set_state(FSMClientWork.work_on)


@router.message(Text(text=LEXICON_KEYBOARDS['stop_forward_messages']), StateFilter(FSMClientWork.work_on))
async def processing_stop_forward(message: Message, state: FSMContext):
    print('processing_stop_forward')
    await state.set_state(FSMClientWork.setting_work)


@router.message(Text(text='Выйти'), StateFilter(FSMClientWork.setting_work, FSMClientWork.work_on))
async def processing_exit(message: Message, state: FSMContext):
    print('processing_exit')
    await message.answer(text='удалить ', reply_markup=ReplyKeyboardRemove(selective=True))
    print('!!!!!!!!!!!!')
    await state.clear()