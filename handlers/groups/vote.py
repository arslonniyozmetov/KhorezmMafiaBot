from aiogram import types, Dispatcher
from utils.misc.session import get_session
from keyboards.inline.vote import vote_start_button, vote_inline_buttons, confirm_keyboard
from collections import Counter
import asyncio

votes = {}
confirm_votes = {"yes": 0, "no": 0}

async def start_voting_pm(chat_id: int):
    session = get_session(chat_id)
    global votes
    votes = {}

    for uid in session["players"].keys():
        try:
            await types.ChatActions.typing()
            await types.Bot.send_message == session["bot"].send_message
            await session["bot"].send_message(
                uid,
                "🗳 Ovoz berish vaqti keldi. Kimni jazolaymiz?",
                reply_markup=vote_inline_buttons(session["players"], uid)
            )
        except:
            pass

    await session["bot"].send_message(chat_id,
        "📢 Aybdorlarni aniqlash va jazolash vaqti keldi.\n45 soniya vaqt bor.",
        reply_markup=vote_start_button()
    )

    await asyncio.sleep(45)
    await conclude_vote(chat_id)

async def vote_action(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    votes[str(call.from_user.id)] = target_id
    await call.message.edit_text(f"✅ Siz {target_id} ni tanladingiz.")

async def conclude_vote(chat_id: int):
    session = get_session(chat_id)
    count = Counter(votes.values())
    if not count:
        return

    top = count.most_common(1)[0]
    session["lynch_candidate"] = top[0]
    name = session["players"].get(top[0], "Noma'lum")
    await session["bot"].send_message(chat_id, f"🔔 {name} eng ko‘p ovoz oldi. Uni osamizmi?", reply_markup=confirm_keyboard())

async def confirm_action(call: types.CallbackQuery):
    answer = call.data.split(":")[1]
    global confirm_votes
    confirm_votes[answer] += 1

    if confirm_votes["yes"] + confirm_votes["no"] >= 3:  # or use len(session["players"])
        session = get_session(call.message.chat.id)
        candidate = session["lynch_candidate"]
        if confirm_votes["yes"] > confirm_votes["no"]:
            name = session["players"].pop(candidate, "Noma’lum")
            session["roles"].pop(candidate, None)
            await call.message.edit_text(f"⚰️ {name} osildi.")
        else:
            await call.message.edit_text("🕊 Ovozlar yetmadi. Hech kim osilmadi.")

        confirm_votes["yes"] = 0
        confirm_votes["no"] = 0

        await asyncio.sleep(3)
        from utils.misc.session import night_phase
        await night_phase(call.message.chat.id)

def register_vote_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(vote_action, lambda c: c.data.startswith("vote:"))
    dp.register_callback_query_handler(confirm_action, lambda c: c.data.startswith("lynch:"))
