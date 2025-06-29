# roles/daydi.py
from base import Role

class Daydi(Role):
    def __init__(self):
        super().__init__(
            name="Daydi",
            description="Tunda kimning uyiga kirsa, u yerga kimlar kelganini (ismlarini) ko'radi.",
            is_active=True
        )
from aiogram import types
from loader import dp
from utils.misc.session import get_session

@dp.callback_query_handler(lambda c: c.data.startswith("daydi:"))
async def handle_daydi_action(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    session = get_session(call.message.chat.id)
    session["night_actions"]["daydi"] = int(target_id)
    await call.message.edit_text("🧟 Siz Daydi sifatida o‘yinchining uyiga bordingiz.")
