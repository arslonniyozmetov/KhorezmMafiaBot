# handlers/groups/vote_handler.py
from aiogram import types
from loader import dp, bot
from utils.misc.session import get_session
from handlers.game.resolve_vote import finalize_vote_confirmation
from handlers.game.end_game import check_win_conditions

@dp.callback_query_handler(lambda c: c.data.startswith("confirm_kill:"))
async def confirm_kill_handler(call: types.CallbackQuery):
    _, target_id, vote_type = call.data.split(":")
    voter_id = call.from_user.id
    session = get_session(call.message.chat.id)

    if "vote_confirmation" not in session:
        return await call.answer("❗ Tasdiqlash bosqichi yo‘q.", show_alert=True)

    if voter_id in session["vote_confirmation"].get("voted_users", []):
        return await call.answer("❌ Siz allaqachon ovoz bergansiz.", show_alert=True)

    if vote_type == "yes":
        session["vote_confirmation"]["yes"] += 1
    else:
        session["vote_confirmation"]["no"] += 1

    session["vote_confirmation"]["voted_users"].append(voter_id)
    await call.answer("✅ Ovozingiz qabul qilindi.")

    # Har galdan so‘ng avtomatik tekshirish
    total_voters = len(session["alive_players"])
    current_votes = len(session["vote_confirmation"]["voted_users"])

    if current_votes >= total_voters:
        # Barcha tiriklar ovoz berdi — yakunlash
        result_text = await finalize_vote_confirmation(call.message.chat.id)
        await bot.send_message(call.message.chat.id, result_text)

        # G‘olib bormi?
        winner = check_win_conditions(call.message.chat.id)
        if winner:
            await bot.send_message(call.message.chat.id, f"🏁 O‘yin tugadi!\n\n{winner}")
