# keyboards/inline/join_game.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def join_game_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🤵🏻 Qo‘shilish", callback_data="join_game"))
    return keyboard
