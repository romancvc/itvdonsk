import os
import uuid
from django.core.management.base import BaseCommand
import telebot
import speech_recognition as sr
from data_one_c.models import Client
from tgbot.models import TgEvent


language = 'ru-RU'
TOKEN = '6108851651:AAFjcdj0PTISgFKrgVfil2QqGfY4hJOctNY'
bot = telebot.TeleBot(TOKEN)
r = sr.Recognizer()
error_recognize = "Извините, я вас не понял. Попробуйте еще раз."



class Command(BaseCommand):

    def handle(self, *args, **options):

        def recognise(filename):
            with sr.AudioFile(filename) as source:
                audio_text = r.listen(source)
                try:
                    text = r.recognize_google(audio_text, language=language)
                    print('Converting audio transcripts into text ...')
                    print(text)
                    return text
                except:
                    return error_recognize

        @bot.message_handler(content_types=['voice'])
        def voice_processing(message):
            filename = str(uuid.uuid4())
            file_name_full = "C:/Users/Nina/PycharmProjects/itvdonsk/itvdonsk/tgbot/management/commands/voice/" + filename + ".ogg"
            file_name_full_converted = "C:/Users/Nina/PycharmProjects/itvdonsk/itvdonsk/tgbot/management/commands/ready/" + filename + ".wav"
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name_full, 'wb') as new_file:
                new_file.write(downloaded_file)
            os.system("ffmpeg -i " + file_name_full + " " + file_name_full_converted)
            text = recognise(file_name_full_converted)
            if text == error_recognize:
                bot.reply_to(message, text)
            else:
                bot_text = "Ваша заявка создана. Текст заявки - "+text
                bot.reply_to(message, bot_text)
                zero_client = Client.objects.get(full_name='Пустой контрагент')
                TgEvent.objects.create(client=zero_client,event_description=text)

            os.remove(file_name_full)
            os.remove(file_name_full_converted)
        bot.polling()