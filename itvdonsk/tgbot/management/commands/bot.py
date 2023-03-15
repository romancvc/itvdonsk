import os
import uuid
from django.core.management.base import BaseCommand
import soundfile as sf
import telebot
import speech_recognition as sr


language = 'ru-RU'
TOKEN = '6108851651:AAFjcdj0PTISgFKrgVfil2QqGfY4hJOctNY'
bot = telebot.TeleBot(TOKEN)
r = sr.Recognizer()


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
                    print('Sorry.. run again...')
                    return "Sorry.. run again..."

        @bot.message_handler(content_types=['voice'])
        def voice_processing(message):
            filename = str(uuid.uuid4())
            file_name_full = "C:/Users/Professional/itvdonsk/itvdonsk/tgbot/management/commands/voice/" + filename + ".ogg"
            file_name_full_converted = "C:/Users/Professional/itvdonsk/itvdonsk/tgbot/management/commands/ready/" + filename + ".wav"
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name_full, 'wb') as new_file:
                new_file.write(downloaded_file)
            os.system("ffmpeg -i " + file_name_full + " " + file_name_full_converted)
            text = recognise(file_name_full_converted)
            bot.reply_to(message, text)
            os.remove(file_name_full)
            os.remove(file_name_full_converted)


        bot.polling()