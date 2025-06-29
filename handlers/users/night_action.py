# handlers/users/night_action.py
from aiogram import types
from loader import dp
from utils.misc.session import get_session

@dp.callback_query_handler(lambda c: c.data.count(":") == 2)
async def handle_night_action(call: types.CallbackQuery):
    role_name, target_id, chat_id = call.data.split(":")
    target_id = int(target_id)
    chat_id = int(chat_id)  # ✅ guruh ID

    session = get_session(chat_id)
    if "night_actions" not in session:
        session["night_actions"] = {}

    session["night_actions"][role_name] = target_id

    from utils.helpers import get_player_name
    name = await get_player_name(call.bot, target_id)
    await call.message.edit_text(f"✅ Siz tanladingiz: <b>{name}</b>", parse_mode="HTML")


