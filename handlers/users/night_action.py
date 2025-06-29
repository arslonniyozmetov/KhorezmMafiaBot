# handlers/users/night_action.py
from aiogram import types
from loader import dp
from utils.misc.session import get_session

@dp.callback_query_handler(lambda c: ":" in c.data)
async def handle_night_action(call: types.CallbackQuery):
    role_name, target_id = call.data.split(":")
    target_id = int(target_id)
    session = get_session(call.message.chat.id)

    if "night_actions" not in session:
        session["night_actions"] = {}

    session["night_actions"][role_name] = target_id
    await call.message.edit_text(f"✅ Siz tanladingiz: <b>{target_id}</b>")
