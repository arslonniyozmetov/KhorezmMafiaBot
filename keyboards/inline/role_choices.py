from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def player_choice_keyboard(prefix: str, players: dict, exclude_id: int = None):
    markup = InlineKeyboardMarkup(row_width=2)
    for uid, name in players.items():
        if uid == exclude_id:
            continue
        markup.add(InlineKeyboardButton(name, callback_data=f"{prefix}:{uid}"))
    return markup
