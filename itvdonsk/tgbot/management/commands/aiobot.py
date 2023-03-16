import os
import uuid
from pathlib import Path

from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, File, Message

import speech_recognition as sr

from data_one_c.models import Client
from tgbot.models import TgEvent
from django.core.management.base import BaseCommand
from django.conf import settings
from .messages import *
from .keyboards import *

storage = MemoryStorage()
bot = Bot(settings.TG_TOKEN)
dp = Dispatcher(bot=bot,
                storage=storage)
r = sr.Recognizer()


class Command(BaseCommand):

    def handle(self, *args, **options):

        @dp.message_handler(commands=['start'])
        async def cmd_start(message: types.Message) -> None:
            await message.answer(text_cmd_start,
                                 reply_markup=start_keyboard(), parse_mode="HTML")

        @dp.callback_query_handler(lambda c: c.data == 'without_authorization')
        async def process_without_authorization(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, text_process_without_authorization1)
            await bot.send_message(callback_query.from_user.id, text_process_without_authorization2,
                                                                parse_mode="HTML",
                                                                reply_markup=authorization_kb())

        @dp.callback_query_handler(lambda c: c.data == 'authorization')
        async def process_authorization(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, text_process_authorization)


        """
        Функция преобразования голосового сообщения в текст

        Attributes
        ----------
        filename : str
            полный путь к файлу конвертированного .wav голосового сообщения

        """
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

        @dp.message_handler(content_types=['voice'])
        async def voice_to_text(message: types.Message):
            voice = await message.voice.get_file()
            path = 'C:/Users/Nina/PycharmProjects/itvdonsk/itvdonsk/tgbot/management/commands/voice/'
            await handle_file(file=voice, file_name=f'{voice.file_id}.ogg', path=path)

            voice_name_full = "C:/Users/Nina/PycharmProjects/itvdonsk/itvdonsk/tgbot/management/commands/voice/" + voice.file_id + ".ogg"
            voice_name_full_converted = "C:/Users/Nina/PycharmProjects/itvdonsk/itvdonsk/tgbot/management/commands/ready/" + voice.file_id + ".wav"
            os.system("ffmpeg -i " + voice_name_full + " " + voice_name_full_converted)
            text = recognise(voice_name_full_converted)

            if text == ERROR_RECOGNISE:
                await message.answer(text)
                os.remove(voice_name_full)
                os.remove(voice_name_full_converted)
            else:
                bot_text = "Ваша заявка создана. Текст заявки - " + text
                await message.answer(bot_text)
                zero_client = Client.objects.get(full_name='Пустой контрагент')
                TgEvent.objects.create(client=zero_client, event_description=text)
                os.remove(voice_name_full)
                os.remove(voice_name_full_converted)\

        executor.start_polling(dp, skip_updates=True)
