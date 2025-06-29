# roles/mashuqa.py
from handlers.roles.base import Role

class Mashuqa(Role):
    def __init__(self):
        super().__init__(
            name="Mashuqa",
            description="Tunda bir o'yinchini bloklaydi. Faol ro'l bo‘lsa, u hech nima qila olmaydi.",
            is_active=True
        )

from aiogram import types
from loader import dp
from utils.misc.session import get_session

@dp.callback_query_handler(lambda c: c.data.startswith("mashuqa:"))
async def handle_mashuqa_action(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    session = get_session(call.message.chat.id)
    session["night_actions"]["mashuqa"] = int(target_id)
    await call.message.edit_text("💋 Siz Mashuqa sifatida kimnidir blokladingiz.")
