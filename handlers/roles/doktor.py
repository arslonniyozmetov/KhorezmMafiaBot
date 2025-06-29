# roles/doktor.py
from handlers.roles.base import Role

class Doktor(Role):
    def __init__(self):
        super().__init__(
            name="Doktor",
            description="Tunda bir kishini davolay oladi.",
            is_active=True
        )
from aiogram import types
from loader import dp
from utils.misc.session import get_session

@dp.callback_query_handler(lambda c: c.data.startswith("doktor:"))
async def handle_doktor_action(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    session = get_session(call.message.chat.id)
    session["night_actions"]["doktor"] = int(target_id)
    await call.message.edit_text("💉 Siz Doktor sifatida tanlov qildingiz.")
