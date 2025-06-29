# utils/helpers.py

from aiogram import Bot
from loader import bot
from aiogram.utils.exceptions import BotBlocked

async def send_pm(user_id: int, text: str, reply_markup=None):
    try:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
    except BotBlocked:
        print(f"❌ PM bloklangan: {user_id}")

async def get_player_name(bot: Bot, user_id: int) -> str:
    try:
        user = await bot.get_chat(user_id)
        return user.full_name
    except:
        return f"User({user_id})"
# utils/helpers.py

async def delete_message_safe(chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        pass
