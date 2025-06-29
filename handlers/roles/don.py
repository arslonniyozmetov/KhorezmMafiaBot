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
    role_name, target_id, chat_id = call.data.split(":")
    target_id = int(target_id)
    chat_id = int(chat_id)

    session = get_session(chat_id)
    session["night_actions"][role_name] = target_id

    from utils.helpers import get_player_name
    name = await get_player_name(call.bot, target_id)
    await call.message.edit_text(f"🕶 Siz Don sifatida tanlov qildingiz: <b>{name}</b>", parse_mode="HTML")

