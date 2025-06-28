import asyncio
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from keyboards.inline.role_choices import player_choice_keyboard
from handlers.groups.vote import start_voting_pm

_sessions = {}

def get_session(chat_id: int):
    chat_id = str(chat_id)
    if chat_id not in _sessions:
        _sessions[chat_id] = {
            "players": {},  # {uid: full_name}
            "roles": {},
            "creator": None,
            "started": False,
            "night_actions": {},
        }
    return _sessions[chat_id]

async def start_game(chat_id: int):
    session = get_session(chat_id)
    if session["started"]:
        return
    session["started"] = True

    players_dict = session["players"]
    players = list(players_dict.values())
    roles = ["Tinch aholi", "Komissar", "Doktor", "Don"][:len(players)]

    await bot.send_message(chat_id, "🎮 O'yin boshlandi!", reply_markup=InlineKeyboardMarkup().add(
        InlineKeyboardButton("Ro‘lingizni bilish", callback_data="show_role")
    ))

    await bot.send_photo(chat_id,
        photo=InputFile("static/main/img/night_khiva.jpg"),
        caption="🌃 *Tun*\nKo‘chaga faqat jasur va qo‘rqmas odamlar chiqishdi...",
        parse_mode="Markdown"
    )

    player_lines = "\n".join([
        f"{i + 1}. <a href='tg://user?id={uid}'>{name}</a>"
        for i, (uid, name) in enumerate(session["players"].items())
    ])
    await bot.send_message(chat_id,
        f"<b>Tirik o‘yinchilar:</b>\n{player_lines}\n\n<b>Ulardan:</b> {', '.join(roles)}",
        parse_mode="HTML"
    )

    await night_phase(chat_id)

async def night_phase(chat_id: int):
    session = get_session(chat_id)
    session["night_actions"] = {}
    players = session["players"]

    # Don
    for uid, role in session["roles"].items():
        if role == "Don":
            await bot.send_message(uid, "🎩 Kimni o‘ldirasiz?", reply_markup=player_choice_keyboard("don", players, uid))

    # Doktor
    for uid, role in session["roles"].items():
        if role == "Doktor":
            await bot.send_message(uid, "💊 Kimni davolaysiz?", reply_markup=player_choice_keyboard("dok", players, uid))

    # Komissar
    for uid, role in session["roles"].items():
        if role == "Komissar":
            kb = InlineKeyboardMarkup().add(
                InlineKeyboardButton("🧐 Tekshirish", callback_data="komissar:check"),
                InlineKeyboardButton("🔫 O‘ldirish", callback_data="komissar:kill")
            )
            await bot.send_message(uid, "👮 Komissar, nima qilasiz?", reply_markup=kb)

    await asyncio.sleep(60)
    await process_night(chat_id)

async def process_night(chat_id: int):
    session = get_session(chat_id)
    don = session["night_actions"].get("don")
    dok = session["night_actions"].get("dok")
    kom_action = session["night_actions"].get("komissar_action")
    kom_target = session["night_actions"].get("komissar")

    killed = None
    if kom_action == "kill" and kom_target and kom_target != dok:
        killed = kom_target
    elif don and don != dok:
        killed = don

    await bot.send_photo(chat_id,
        photo=InputFile("static/main/img/day_khiva.jpg"),
        caption="🌅 *Xayrli tong!*\nShamollar mish-mishlarni shaharga yetkazdi...",
        parse_mode="Markdown"
    )

    if killed:
        name = session["players"].pop(killed, "Noma'lum")
        session["roles"].pop(killed, None)
        await bot.send_message(chat_id, f"❌ {name} tunda halok bo‘ldi.")
    else:
        await bot.send_message(chat_id, "😌 Bu tunda hech kim halok bo‘lmadi.")

    await asyncio.sleep(3)
    await start_voting_pm(chat_id)
