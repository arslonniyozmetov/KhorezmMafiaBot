from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def vote_keyboard(players, exclude_id=None):
    markup = InlineKeyboardMarkup(row_width=2)
    for uid, name in players.items():
        if str(uid) != str(exclude_id):
            markup.add(InlineKeyboardButton(name, callback_data=f"vote:{uid}"))
    return markup



def confirm_keyboard() -> InlineKeyboardMarkup:
    """
    Ovoz natijasini tasdiqlash uchun tugmalar.
    """
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("✅ Ha", callback_data="lynch:yes"),
        InlineKeyboardButton("❌ Yo‘q", callback_data="lynch:no")
    )
