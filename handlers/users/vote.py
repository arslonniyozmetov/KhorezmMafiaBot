# handlers/users/vote.py
from aiogram import types
from loader import dp, bot
from utils.misc.session import get_session

@dp.callback_query_handler(lambda c: c.data.startswith("vote:"))
async def handle_vote(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    voter_id = call.from_user.id
    session = get_session(call.message.chat.id)

    if voter_id in session["votes"]:
        return await call.answer("Siz allaqachon ovoz berdingiz.", show_alert=True)

    session["votes"][voter_id] = int(target_id)

    await call.message.edit_text(f"🗳️ Siz tanladingiz: {target_id}")

    # E’lon qilish: kim kimga ovoz berdi
    await bot.send_message(
        call.message.chat.id,
        f"🧾 <a href='tg://user?id={voter_id}'>O‘yinchi</a> ➡️ <b>{target_id}</b> ga ovoz berdi."
    )
