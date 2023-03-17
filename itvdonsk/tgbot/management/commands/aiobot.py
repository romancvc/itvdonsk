import os
import uuid
from pathlib import Path

from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, File, Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

import speech_recognition as sr
from asgiref.sync import sync_to_async

from data_one_c.models import Client
from tgbot.models import TgEvent, TgUser
from django.core.management.base import BaseCommand
from django.conf import settings
from .messages import *
from .keyboards import *
from .request_db import *

storage = MemoryStorage()
bot = Bot(settings.TG_TOKEN)
dp = Dispatcher(bot=bot,
                storage=storage)
r = sr.Recognizer()

chat_id = ''
username = ''


class UserStates(StatesGroup):
    enter_password = State()
    choosing_action = State()
    submitrequest = State()


class Command(BaseCommand):

    def handle(self, *args, **options):

        @dp.message_handler(commands=['start'])
        async def cmd_start(message: types.Message) -> None:
            global chat_id, username
            chat_id=message.chat.id
            username = message.from_user.username
            await sync_to_async(TgUser.objects.get_or_create)(external_id=chat_id,nickname=username)
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
            all_passwords = process_authorization_all_passwords_sync()
            if message.text in str(all_passwords):
                this_company = process_authorization_this_company_sync(text=message.text)
                process_authorization_sync(chat_id, this_company)
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
                    TgEvent.objects.create(client=Client.objects.get(full_name='Пустой контрагент'),
                                           event_description=text)
                    await message.answer(bot_text)
                else:
                    TgEvent.objects.create(client=Client.objects.get(id=this_client),
                                           event_description=text)
                    await message.answer(bot_text)
                await state.reset()
                os.remove(voice_name_full)
                os.remove(voice_name_full_converted)

        executor.start_polling(dp, skip_updates=True)
