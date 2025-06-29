from aiogram import types
from loader import dp
from utils.misc.session import get_session
from keyboards.inline.join_game import join_game_keyboard

@dp.message_handler(commands=["game"], chat_type=["group", "supergroup"])
async def game_command(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    session = get_session(chat_id)

    if session["game_started"]:
        return await message.reply("⚠️ O‘yin allaqachon boshlangan.")

    # 🔄 O'yinni tozalaymiz va yangidan boshlaymiz
    session["players"] = []
    session["game_started"] = False
    session["host_id"] = user_id  # O‘yinni kim boshlaganini saqlaymiz

    await message.reply(
        f"🎮 <a href='tg://user?id={user_id}'>{message.from_user.full_name}</a> yangi o‘yin yaratdi!\n\n"
        f"Quyidagi tugma orqali o‘yinga qo‘shiling:",
        parse_mode="HTML",
        reply_markup=join_game_keyboard()
    )
