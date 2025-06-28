from aiogram import Dispatcher, types
from data import config
from keyboards.inline.join_game import join_game_keyboard
from utils.misc.session import get_session, start_game
import asyncio

# game_command ni o‘zgartirmasdan, start_game chaqirilganda xabar o‘zgartiriladi
async def game_command(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        return await message.reply("Bu buyruq faqat guruhda ishlaydi.")

    session = get_session(message.chat.id)
    if session["started"]:
        return await message.reply("O‘yin allaqachon boshlangan.")

    session.update({
        "players": {},
        "roles": {},
        "creator": message.from_user.id,
        "started": False,
        "night_actions": {},
    })

    try:
        await message.delete()
    except Exception as e:
        print(f"Xabarni o‘chirishda xatolik: {e}")

    join_message = await message.answer(
        "🎮 Mafia o‘yini boshlandi! Tugmani bosib qo‘shiling:",
        reply_markup=join_game_keyboard()
    )

    # join_message ni sessionga saqlaymiz
    session["join_message_id"] = join_message.message_id

    await asyncio.sleep(30)

    if not session["started"]:
        if len(session["players"]) < 4:
            try:
                await join_message.delete()
            except Exception as e:
                print(f"Qo‘shilish xabarini o‘chirishda xatolik: {e}")
            await message.bot.send_message(
                message.chat.id,
                "O'yinni boshlash uchun o'yinchilar yetarli emas...."
            )
        else:
            await start_game(message.chat.id)


async def start_command(message: types.Message):
    session = get_session(message.chat.id)

    if message.from_user.id != session["creator"] and message.from_user.id not in config.ADMINS:
        return None

    await start_game(message.chat.id)




def register_game_handlers(dp: Dispatcher):
    dp.register_message_handler(game_command, commands=["game"], state="*")
    dp.register_message_handler(start_command, commands=["start"], state="*")

from aiogram import types
from loader import dp
from utils.misc.session import get_session

from aiogram import types
from loader import dp
from utils.misc.session import get_session
from keyboards.inline.join_game import join_game_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram import types
from loader import dp
from utils.misc.session import get_session

from aiogram import types
from loader import dp
from utils.misc.session import get_session

from aiogram import types
from loader import dp
from utils.misc.session import get_session
from keyboards.inline.join_game import join_game_keyboard

@dp.callback_query_handler(lambda c: c.data == "join_game")
async def join_game_callback(call: types.CallbackQuery):
    session = get_session(call.message.chat.id)
    user_id = call.from_user.id

    if user_id in session["players"]:
        await call.answer("Siz allaqachon o‘yindasiz.")
        return

    session["players"][user_id] = call.from_user.full_name

    # Ismlar ro‘yxatini tayyorlash
    players_html = ", ".join(
        f"<a href='tg://user?id={uid}'>{name}</a>"
        for uid, name in session["players"].items()
    )

    text = (
        f"Ro'yxatdan o'tganlar:\n\n"
        f"{players_html}\n\n"
        f"Jami: {len(session['players'])} ta"
    )

    # 🔥 MUHIM: reply_markup=join_game_keyboard() orqali tugmani saqlash
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=join_game_keyboard())
    await call.answer("✅ Siz o‘yinga qo‘shildingiz!")

