from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def vote_start_button():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("🗳 Ovoz berish", callback_data="vote:start")
    )

def vote_inline_buttons(players: dict, voter_id):
    markup = InlineKeyboardMarkup(row_width=1)
    for uid, name in players.items():
        if str(uid) != str(voter_id):
            markup.add(InlineKeyboardButton(name, callback_data=f"vote:{uid}"))
    return markup

def confirm_keyboard():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Ha", callback_data="lynch:yes"),
        InlineKeyboardButton("❌ Yo‘q", callback_data="lynch:no")
    )
