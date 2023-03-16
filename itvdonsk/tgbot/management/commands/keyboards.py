from aiogram.types import ContentType, File, Message, \
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup


def authorization_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kb.add(InlineKeyboardButton('Авторизация', callback_data='authorization'))

    return kb

def start_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kb.add(InlineKeyboardButton('Авторизация', callback_data='authorization'))
    kb.add(InlineKeyboardButton('Продолжить без авторизации', callback_data='without_authorization'))

    return kb