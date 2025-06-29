# handlers/roles/don.py
from aiogram import types
from loader import dp
from utils.misc.session import get_session

class Don:
    name = "Don"
    description = "Mafiyaning boshlig‘i. Har tunda kimnidir o‘ldiradi."
    is_mafia = True
    is_active = True

@dp.callback_query_handler(lambda c: c.data.startswith("don:"))
async def handle_don_action(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    session = get_session(call.message.chat.id)
    session["night_actions"]["don"] = int(target_id)

    await call.message.edit_text("🕶 Siz Don sifatida tanlov qildingiz.")
