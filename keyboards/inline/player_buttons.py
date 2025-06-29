# keyboards/inline/player_buttons.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.helpers import get_player_name

async def player_keyboard(player_ids, exclude=None):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for pid in player_ids:
        if pid == exclude:
            continue
        name = await get_player_name(pid)
        keyboard.add(InlineKeyboardButton(text=name, callback_data=f"target:{pid}"))
    return keyboard
