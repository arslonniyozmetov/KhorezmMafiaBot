# game/night_circle.py
from loader import bot
from utils.misc.session import get_session
from utils.helpers import send_pm
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.roles.base import Role
from data.config import ADMINS

def generate_action_keyboard(role_name, players, exclude_id):
    kb = InlineKeyboardMarkup()
    for pid in players:
        if pid == exclude_id:
            continue
        kb.add(InlineKeyboardButton(f"👤 {pid}", callback_data=f"{role_name}:{pid}"))
    return kb

async def start_night_phase(chat_id: int):
    session = get_session(chat_id)
    session["phase"] = "night"
    session["night_actions"] = {}

    players = session["alive_players"]
    role_map = session["roles"]

    for player_id in players:
        role: Role = role_map.get(player_id)
        if not role or not role.is_active:
            continue

        kb = generate_action_keyboard(role.name.lower(), players, player_id)
        try:
            await send_pm(
                player_id,
                f"🌙 TUN: Sizning ro‘lingiz – <b>{role.name}</b>\nIltimos, kimga harakat qilasiz?",
                reply_markup=kb
            )
        except:
            await bot.send_message(ADMINS[0], f"⚠️ <a href='tg://user?id={player_id}'>PM yuborilmadi</a>")

import asyncio
from handlers.game.resolve_night import resolve_night

async def start_night_phase(chat_id: int):
    ...
    await bot.send_message(chat_id, "🌙 TUN bosqichi boshlandi. 30 soniya kutamiz...")
    await asyncio.sleep(30)

    result = await resolve_night(chat_id)
    await bot.send_message(chat_id, result)
