from aiogram import Dispatcher, types

from loader import dp
from utils.misc.session import get_session
from keyboards.inline.vote import vote_keyboard, confirm_keyboard
import asyncio
from collections import Counter

votes = {}
lynch_votes = {"yes": 0, "no": 0}


# Ovoz berishni boshlash
async def start_voting(chat_id: int):
    session = get_session(chat_id)
    global votes
    votes = {}

    # PM orqali ovoz berish tugmalari
    for uid, name in session["players"].items():
        try:
            await session["bot"].send_message(
                uid,
                "🗳 Ovoz bering. Kimni jazolash kerak?",
                reply_markup=vote_keyboard(session["players"], exclude_id=int(uid))
            )
        except:
            continue

    # Guruhga umumiy xabar
    await session["bot"].send_message(
        chat_id,
        "🔔 Aybdorlarni aniqlash va jazolash vaqti keldi.\nOvoz berish uchun 45 soniya.",
    )

    await asyncio.sleep(45)
    await conclude_vote(chat_id)


# Ovoz berish tugmasi bosilganda
@dp.callback_query_handler(lambda c: c.data.startswith("vote:"))
async def vote_action(call: types.CallbackQuery):
    session = get_session(call.from_user.id)  # PM bo‘lgani uchun user_id orqali

    _, target_id = call.data.split(":")
    voter_id = str(call.from_user.id)

    # Ovozni saqlash
    votes[voter_id] = target_id

    # Tugmani edit qilish
    name = session["players"].get(target_id, "Noma‘lum")
    await call.message.edit_text(f"✅ Siz {name} ni tanladingiz.")

    # Agar barcha tirik o‘yinchilar ovoz bergan bo‘lsa
    if len(votes) >= len(session["players"]):
        await conclude_vote(session["group_id"])



# Ovozlarni hisoblash
async def conclude_vote(chat_id: int):
    session = get_session(chat_id)
    vote_counts = Counter(votes.values())

    if not vote_counts:
        await session["bot"].send_message(chat_id, "😐 Hech kim ovoz bermadi.")
        return

    top = vote_counts.most_common(1)[0]
    candidate_name = top[0]

    session["lynch_candidate"] = candidate_name
    global lynch_votes
    lynch_votes = {"yes": 0, "no": 0}

    await session["bot"].send_message(
        chat_id,
        f"🔔 {candidate_name} eng ko‘p ovoz oldi. Uni osamizmi?",
        reply_markup=confirm_keyboard()
    )


# Tasdiqlash tugmalari bosilganda
async def confirm_lynch(call: types.CallbackQuery):
    global lynch_votes
    decision = call.data.split(":")[1]
    lynch_votes[decision] += 1

    session = get_session(call.message.chat.id)
    total_votes = sum(lynch_votes.values())

    if total_votes >= len(session["players"]):
        if lynch_votes["yes"] > lynch_votes["no"]:
            candidate_name = session.get("lynch_candidate")
            remove_id = None
            for uid, name in session["players"].items():
                if name == candidate_name:
                    remove_id = uid
                    break

            if remove_id:
                session["players"].pop(remove_id, None)
                session["roles"].pop(remove_id, None)

            await call.message.edit_text(f"⚰️ {candidate_name} osildi.")
        else:
            await call.message.edit_text("😌 Ovoz yetmadi. Hech kim osilmadi.")

        await asyncio.sleep(5)
        from utils.misc.session import night_phase
        await night_phase(call.message.chat.id)
    else:
        await call.answer(f"Ovoz qabul qilindi. Ha: {lynch_votes['yes']}, Yo‘q: {lynch_votes['no']}")


# Ro'yxatdan o'tkazish
def register_vote_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(vote_action, lambda c: c.data.startswith("vote:"))
    dp.register_callback_query_handler(confirm_lynch, lambda c: c.data.startswith("lynch:"))
