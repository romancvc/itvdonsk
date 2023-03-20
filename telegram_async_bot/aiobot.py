import os
import time
import uuid
from pathlib import Path

from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, File, Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import Throttled
from subprocess import DEVNULL, STDOUT, check_call

import speech_recognition as sr
from django.conf import settings

from messages import *
from keyboards import *
from postgres_req import *


storage = MemoryStorage()
bot = Bot('6108851651:AAFjcdj0PTISgFKrgVfil2QqGfY4hJOctNY')
dp = Dispatcher(bot=bot,
                storage=storage)
r = sr.Recognizer()

chat_id = ''
username = ''


class UserStates(StatesGroup):
    enter_password = State()
    choosing_action = State()
    submit_request = State()


async def check_authorization():
    global chat_id
    result = await check_authorization_bd(chat_id)
    if result:
        return True
    else:
        return False


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    global chat_id, username
    chat_id = message.chat.id
    username = message.from_user.username
    result = await cmd_start_db(chat_id, username)
    result2 = await check_authorization()
    if result:
        await message.answer(text_cmd_start,
                             reply_markup=start_keyboard(), parse_mode="HTML")
        return
    else:
        if result2:
            await message.answer(text_cmd_start_with_authorization, parse_mode="HTML")
            await UserStates.submit_request.set()
            return
        else:
            await message.answer('Вы не авторизованы. Нажмите кнопку ниже, чтобы авторизоваться.',
                                 reply_markup=start_keyboard(), parse_mode="HTML")
            return


@dp.callback_query_handler(lambda c: c.data == 'without_authorization', state='*')
async def process_without_authorization(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(UserStates.submit_request)
    await bot.send_message(callback_query.from_user.id, text_process_without_authorization1)
    await asyncio.sleep(2)
    await bot.send_message(callback_query.from_user.id, text_process_without_authorization2,
                           parse_mode="HTML")
    await asyncio.sleep(2)
    await bot.send_message(callback_query.from_user.id, text_process_without_authorization3,
                           parse_mode="HTML", reply_markup=authorization_kb())


@dp.callback_query_handler(lambda c: c.data == 'authorization', state='*')
async def process_authorization_start(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text_process_authorization)
    await bot.send_contact(callback_query.from_user.id, phone_number='+7(938)146-41-00', first_name='ООО "Бизнес решения"')
    await UserStates.enter_password.set()


@dp.message_handler(state=UserStates.enter_password)
async def process_authorization(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    result = await process_authorization_db(text=message.text, chat_id=chat_id)
    if result:
        await message.answer("Вы успешно авторизировались!")
        await message.answer(text_with_authorization, parse_mode="HTML")
        await UserStates.submit_request.set()
    else:
        await message.answer('Вы ввели неверный пароль! Попробуйте еще раз или обратитесь в поддержку.')
        await UserStates.enter_password.set()
    await state.update_data()


@dp.message_handler(state=UserStates.choosing_action)
async def choosing_actions(message: types.Message, state: FSMContext):
    await UserStates.next()
    await bot.send_message(text_with_authorization)


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer('Вы вышли из диалога. Введие или нажмите 👉🏻 /start')
    await state.finish()


def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language='ru_RU')
            return text
        except:
            return ERROR_RECOGNISE


async def handle_file(file: types.File, file_name: str, path: str):
    Path(f'{path}').mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f'{path}/{file_name}')


async def anti_flood(message: types.Message, state: FSMContext, *args, **kwargs):
    await message.answer(f'Вы уже оставили заявку. Следующую заявку можно оставить не раньше, чем через {remaining_time}!\n\n'
                         f'Для выхода в главное меню введите или нажмите 👉🏻 /start')
    await state.finish()


@dp.message_handler(content_types=['voice'], state=UserStates.submit_request)
@dp.throttled(anti_flood, rate=3600)
async def voice_to_text(message: types.Message, state: FSMContext):
    global chat_id, start_anti_flood_time
    chat_id=message.chat.id
    voice = await message.voice.get_file()
    path = 'C:/Users/Professional/itvdonsk2/telegram_async_bot/voice/'
    await handle_file(file=voice, file_name=f'{voice.file_id}.ogg', path=path)
    voice_name_full = "C:/Users/Professional/itvdonsk2/telegram_async_bot/voice/" + voice.file_id + ".ogg"
    voice_name_full_converted = "C:/Users/Professional/itvdonsk2/telegram_async_bot/ready/" + voice.file_id + ".wav"
    check_call(['ffmpeg', '-i', voice_name_full, voice_name_full_converted], stdout=DEVNULL, stderr=STDOUT)
    text = recognise(voice_name_full_converted)

    if text == ERROR_RECOGNISE:
        await message.answer(text)
    else:
        await voice_to_text_db(chat_id, text)
        await message.answer(bot_text, parse_mode="HTML")
    os.remove(voice_name_full)
    os.remove(voice_name_full_converted)
    await asyncio.sleep(3)
    await message.answer(after_submit, parse_mode="HTML")
    await state.finish()

executor.start_polling(dp, skip_updates=True)
