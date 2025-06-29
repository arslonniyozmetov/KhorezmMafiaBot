# roles/komissar.py
from handlers.roles.base import Role

class Komissar(Role):
    def __init__(self):
        super().__init__(
            name="Komissar",
            description="Har tunda bir o'yinchining ro'lini tekshiradi.",
            is_active=True
        )
from aiogram import types
from loader import dp
from utils.misc.session import get_session

@dp.callback_query_handler(lambda c: c.data.startswith("komissar:"))
async def handle_komissar_action(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    session = get_session(call.message.chat.id)
    session["night_actions"]["komissar"] = int(target_id)
    await call.message.edit_text("🕵️ Siz Komissar sifatida tanlov qildingiz.")