# roles/qotil.py
from handlers.roles.base import Role

class Qotil(Role):
    def __init__(self):
        super().__init__(
            name="Qotil",
            description="Har kecha bir kishini o‘ldiradi. Faqat o‘zi tirik qolsa yutadi.",
            is_active=True,
            is_neutral=True
        )
from aiogram import types
from loader import dp
from utils.misc.session import get_session

@dp.callback_query_handler(lambda c: c.data.startswith("qotil:"))
async def handle_qotil_action(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    session = get_session(call.message.chat.id)
    session["night_actions"]["qotil"] = int(target_id)
    await call.message.edit_text("🔪 Siz Qotil sifatida tanlov qildingiz.")
