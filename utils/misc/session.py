from loader import bot
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from keyboards.inline.role_choices import player_choice_keyboard

_sessions = {}


def get_session(chat_id):
    chat_id = str(chat_id)
    if chat_id not in _sessions:
        _sessions[chat_id] = {
            "players": {},
            "roles": {},
            "creator": None,
            "started": False,
            "night_actions": {},
            "join_message_id": None,
            "bot": bot
        }
    return _sessions[chat_id]


async def start_game(chat_id: int):
    session = get_session(chat_id)
    if session["started"]: return
    session["started"] = True

    players_dict = session["players"]
    players = list(players_dict.values())
    roles = ["Tinch aholi", "Komissar", "Doktor", "Don"][:len(players)]

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Rolingizni bilish", callback_data="show_role")
    )
    await bot.send_message(chat_id, "🎮 O'yin boshlandi!", reply_markup=keyboard)

    await bot.send_photo(chat_id, InputFile("static/main/img/night_khiva.jpg"),
                         caption="🌃 <b>Tun boshlandi</b>\nJasur va qo‘rqmaslar uchun...")

    players_html = "\n".join([
        f"{i + 1}. <a href='tg://user?id={uid}'>{name}</a>"
        for i, (uid, name) in enumerate(players_dict.items())
    ])
    await bot.send_message(chat_id, f"<b>Tirik o‘yinchilar:</b>\n{players_html}\n\n<b>Ulardan:</b> {', '.join(roles)}",
                           parse_mode="HTML")

    await night_phase(chat_id)


async def night_phase(chat_id):
    session = get_session(chat_id)
    session["night_actions"] = {}

    for uid, role in session["roles"].items():
        if role == "Don":
            await bot.send_message(uid, "🎩 Kimni o‘ldirasiz?",
                                   reply_markup=player_choice_keyboard("don", session["players"], uid))
        if role == "Doktor":
            await bot.send_message(uid, "💊 Kimni davolaysiz?",
                                   reply_markup=player_choice_keyboard("dok", session["players"], uid))
        if role == "Komissar":
            kb = InlineKeyboardMarkup()
            kb.add(
                InlineKeyboardButton("🧐 Tekshirish", callback_data="komissar:check"),
                InlineKeyboardButton("🔫 O‘ldirish", callback_data="komissar:kill")
            )
            await bot.send_message(uid, "👮 Komissar, nima qilasiz?", reply_markup=kb)

    await asyncio.sleep(60)
    await process_night(chat_id)


async def process_night(chat_id):
    session = get_session(chat_id)
    don = session["night_actions"].get("don")
    dok = session["night_actions"].get("dok")
    kom_action = session["night_actions"].get("komissar_action")
    kom_target = session["night_actions"].get("komissar")

    killed = None
    if kom_action == "kill" and kom_target != dok:
        killed = kom_target
    elif don and don != dok:
        killed = don

    await bot.send_photo(chat_id, InputFile("static/main/img/day_khiva.jpg"), caption="🌅 <b>Xayrli tong!</b>",
                         parse_mode="HTML")

    if killed:
        name = session["players"].pop(killed, "Noma’lum")
        session["roles"].pop(killed, None)
        await bot.send_message(chat_id, f"❌ Tunda {name} halok bo‘ldi.")
    else:
        await bot.send_message(chat_id, "🌅 Bu tunda hech kim halok bo‘lmadi.")

    await asyncio.sleep(5)
    from handlers.groups.vote import start_voting
    await start_voting(chat_id)
