# game/resolve_vote.py
from collections import Counter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot
from utils.misc.session import get_session
from utils.helpers import get_player_name

def generate_like_dislike_keyboard(target_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("👍 Ha", callback_data=f"confirm_kill:{target_id}:yes"),
        InlineKeyboardButton("👎 Yo‘q", callback_data=f"confirm_kill:{target_id}:no")
    )
    return kb

def get_most_voted(votes: dict):
    if not votes:
        return None, 0
    counter = Counter(votes.values())
    most_common = counter.most_common(1)[0]
    return most_common[0], most_common[1]

async def resolve_vote(chat_id: int):
    session = get_session(chat_id)
    votes = session.get("votes", {})

    target_id, count = get_most_voted(votes)
    if not target_id:
        return None, "⚠️ Hech kimga ovoz berilmadi."

    session["vote_confirmation"] = {
        "target_id": target_id,
        "yes": 0,
        "no": 0,
        "voted_users": []
    }

    kb = generate_like_dislike_keyboard(target_id)
    player_name = await get_player_name(bot, target_id)
    text = f"⚖️ Eng ko‘p ovoz olgan: <b>{player_name}</b>\nChiqarishni tasdiqlaysizmi?"

    return kb, text


# 👇 Bu alohida chaqiriladigan yakunlovchi funksiya
async def finalize_vote_confirmation(chat_id: int):
    session = get_session(chat_id)
    data = session.get("vote_confirmation")

    if not data:
        return "❌ Hali tasdiqlash mavjud emas."

    yes = data["yes"]
    no = data["no"]
    target_id = int(data["target_id"])
    alive = session["alive_players"]
    roles = session["roles"]

    if yes > no:
        result = f"✅ <b>{target_id}</b> o‘yindan chiqarildi."
        if target_id in alive:
            alive.remove(target_id)
        # Kamikadze bo‘lsa — boshqa birini o‘ldiradi
        role = roles.get(target_id)
        if role and role.name.lower() == "kamikadze":
            # kimga ko‘proq ovoz berganini topamiz
            victim_counter = Counter(session["votes"].values())
            victim_counter.pop(target_id, None)  # o‘zidan tashqari
            if victim_counter:
                victim_id, _ = victim_counter.most_common(1)[0]
                if victim_id in alive:
                    alive.remove(victim_id)
                    result += f"\n💥 Kamikadze o‘zi bilan <b>{victim_id}</b> ni ham olib ketdi!"
    else:
        result = f"🚫 <b>{target_id}</b> chiqarilmadi. Ovozlar yetarli emas."

    session["alive_players"] = alive
    session["vote_confirmation"] = {}
    session["votes"] = {}

    return result
