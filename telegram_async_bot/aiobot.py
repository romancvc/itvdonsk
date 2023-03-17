import os
import uuid
from pathlib import Path
import sqlite3

from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, File, Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

import speech_recognition as sr

from messages import *
from keyboards import *

storage = MemoryStorage()
bot = Bot('6108851651:AAFjcdj0PTISgFKrgVfil2QqGfY4hJOctNY')
dp = Dispatcher(bot=bot,
                storage=storage)
r = sr.Recognizer()
conn = sqlite3.connect(r'C:\Users\Nina\PycharmProjects\itvdonsk\itvdonsk\db.sqlite3')
cur = conn.cursor()

chat_id = ''
username = ''


class UserStates(StatesGroup):
    enter_password = State()
    choosing_action = State()
    submitrequest = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    global chat_id
    global username
    chat_id=message.chat.id
    username = message.from_user.username
    try:
        cur.execute(f"INSERT INTO tgbot_tguser (external_id, nickname) VALUES ({chat_id}, '{username}')")
        conn.commit()
    except:
        return
    await message.answer(text_cmd_start,
                         reply_markup=start_keyboard(), parse_mode="HTML")


@dp.callback_query_handler(lambda c: c.data == 'without_authorization')
async def process_without_authorization(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(UserStates.submitrequest)
    await bot.send_message(callback_query.from_user.id, text_process_without_authorization1)
    await bot.send_message(callback_query.from_user.id, text_process_without_authorization2,
                                                        parse_mode="HTML",
                                                        reply_markup=authorization_kb())


@dp.callback_query_handler(lambda c: c.data == 'authorization')
async def process_authorization_start(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text_process_authorization)
    await state.set_state(UserStates.enter_password)


@dp.message_handler(state=UserStates.enter_password)
async def process_authorization(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    nickanme = message.from_user.username
    all_passwords = Client.objects.values_list('tg_password', flat=True)
    if message.text in all_passwords:
        this_company = Client.objects.values_list('id', flat=True).get(tg_password=message.text)
        TgUser.objects.filter(external_id=chat_id).update(
            company=this_company
        )
        await message.answer("Вы успешно авторизировались!")
        await state.set_state(UserStates.submitrequest)
        await message.answer(text_with_authorization, parse_mode="HTML")
    else:
        await message.answer('Вы ввели неверный пароль! Попробуйте еще раз или обратитесь в поддержку.')
        await state.set_state(UserStates.enter_password)
    await state.update_data()


@dp.message_handler(state=UserStates.choosing_action)
async def choosing_actions(message: types.Message, state: FSMContext):
    await UserStates.next()
    await bot.send_message(text_with_authorization)


def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language=settings.LANGUAGE_CODE)
            return text
        except:
            return ERROR_RECOGNISE


async def handle_file(file: types.File, file_name: str, path: str):
    Path(f'{path}').mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f'{path}/{file_name}')


@dp.message_handler(content_types=['voice'], state=UserStates.submitrequest)
async def voice_to_text(message: types.Message, state: FSMContext):
    global chat_id
    chat_id=message.chat.id
    voice = await message.voice.get_file()
    path = 'C:/Users/Nina/PycharmProjects/itvdonsk/itvdonsk/tgbot/management/commands/voice/'
    await handle_file(file=voice, file_name=f'{voice.file_id}.ogg', path=path)

    voice_name_full = "C:/Users/Nina/PycharmProjects/itvdonsk/itvdonsk/tgbot/management/commands/voice/" + voice.file_id + ".ogg"
    voice_name_full_converted = "C:/Users/Nina/PycharmProjects/itvdonsk/itvdonsk/tgbot/management/commands/ready/" + voice.file_id + ".wav"
    os.system("ffmpeg -i " + voice_name_full + " " + voice_name_full_converted)
    text = recognise(voice_name_full_converted)

    if text == ERROR_RECOGNISE:
        await message.answer(text)
    else:
        zero_client = Client.objects.values_list('id', flat=True).get(full_name='Пустой контрагент')
        this_client = TgUser.objects.values_list('company', flat=True).get(external_id=chat_id)
        if this_client==zero_client:
            await message.answer(bot_text)
            TgEvent.objects.create(client=Client.objects.get(full_name='Пустой контрагент'),
                                   event_description=text)
        else:
            await message.answer(bot_text)
            TgEvent.objects.create(client=Client.objects.get(id=this_client)
                                   , event_description=text)
        await state.reset()
        os.remove(voice_name_full)
        os.remove(voice_name_full_converted)

executor.start_polling(dp, skip_updates=True)
