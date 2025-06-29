# game/voting.py

from loader import bot
from utils.helpers import send_pm, get_player_name
from utils.misc.session import get_session
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from handlers.game.resolve_vote import resolve_vote, finalize_vote_confirmation
from handlers.game.end_game import check_win_conditions

# 🗳 Ovoz berish uchun tugma generator
async def generate_vote_keyboard(chat_id: int, exclude_id: int):
    session = get_session(chat_id)
    kb = InlineKeyboardMarkup()
    for pid in session["alive_players"]:
        if pid == exclude_id:
            continue
        name = await get_player_name(bot, pid)
        kb.add(InlineKeyboardButton(f"👤 {name}", callback_data=f"vote:{pid}"))
    return kb

# 🚀 Ovoz berishni boshlash
async def start_day_phase(chat_id: int):
    session = get_session(chat_id)
    session["phase"] = "day"
    session["votes"] = {}

    await bot.send_message(chat_id, "📩 Ovoz berish boshlandi. Har bir o‘yinchi PM orqali ovoz beradi. 30 soniya beriladi.")

    for voter in session["alive_players"]:
        kb = await generate_vote_keyboard(chat_id, voter)
        try:
            await send_pm(voter, "🗳 Kimni o‘yindan chiqarishni xohlaysiz?", reply_markup=kb)
        except:
            await bot.send_message(chat_id, f"⚠️ <a href='tg://user?id={voter}'>PM yuborilmadi</a>", parse_mode="HTML")

    # 🕒 30 soniya kutamiz
    await asyncio.sleep(30)

    # 🧮 Ovozlarni hisoblaymiz
    kb, text = await resolve_vote(chat_id)
    if kb:
        msg = await bot.send_message(chat_id, text, reply_markup=kb)

        # ✅ 30 soniya qaror bosqichi
        await asyncio.sleep(30)
        result = await finalize_vote_confirmation(chat_id)
        await bot.send_message(chat_id, result)

        # 🏆 G‘olibni tekshiramiz
        winner = check_win_conditions(chat_id)
        if winner:
            await bot.send_message(chat_id, f"🏁 O‘yin tugadi!\n\n{winner}")
