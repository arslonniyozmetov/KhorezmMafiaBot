# game/voting.py
from loader import bot
from utils.helpers import send_pm, get_player_name
from utils.misc.session import get_session
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_vote_keyboard(chat_id: int, exclude_id: int):
    session = get_session(chat_id)
    kb = InlineKeyboardMarkup()
    for pid in session["alive_players"]:
        if pid == exclude_id:
            continue
        kb.add(InlineKeyboardButton(f"👤 {pid}", callback_data=f"vote:{pid}"))
    return kb

async def start_voting(chat_id: int):
    session = get_session(chat_id)
    session["phase"] = "voting"
    session["votes"] = {}

    for voter in session["alive_players"]:
        kb = generate_vote_keyboard(chat_id, voter)
        try:
            await send_pm(voter, "📩 Kimni chiqarishni xohlaysiz? Tanlang:", reply_markup=kb)
        except:
            await bot.send_message(chat_id, f"⚠️ <a href='tg://user?id={voter}'>PM yuborilmadi</a>")

import asyncio
from handlers.game.resolve_vote import resolve_vote, finalize_vote_confirmation
from handlers.game.end_game import check_win_conditions

async def start_voting(chat_id: int):
    ...
    await bot.send_message(chat_id, "📩 Ovoz berish boshlandi. 30 soniya ichida ovoz bering.")
    await asyncio.sleep(30)

    kb, text = await resolve_vote(chat_id)
    if kb:
        msg = await bot.send_message(chat_id, text, reply_markup=kb)
        # U ham 30 soniyada tugaydi
        await asyncio.sleep(30)
        result = await finalize_vote_confirmation(chat_id)
        await bot.send_message(chat_id, result)

        # G‘olibni tekshiramiz
        winner = check_win_conditions(chat_id)
        if winner:
            await bot.send_message(chat_id, f"🏁 O‘yin tugadi!\n\n{winner}")
