from aiogram import Dispatcher, types
from aiogram.utils.exceptions import MessageNotModified

from loader import dp
from utils.misc.session import get_session
from keyboards.inline.join_game import join_game_keyboard

@dp.callback_query_handler(lambda c: c.data == "join_game")
async def join_game_callback(call: types.CallbackQuery):
    session = get_session(call.message.chat.id)
    user = call.from_user

    if not session or session["started"]:
        return await call.answer("O‘yin allaqachon boshlangan yoki mavjud emas.")

    if str(user.id) in session["players"]:
        return await call.answer("Siz allaqachon o‘yinga qo‘shilgansiz.")

    # ✅ Qo‘shamiz
    session["players"][str(user.id)] = user.full_name
    await call.answer("✅ O‘yinga qo‘shildingiz!")

    # ✅ O‘yinchilarning ro‘yxatini HTML ko‘rinishda tayyorlaymiz
    players_html = ", ".join(
        f"<a href='tg://user?id={uid}'>{name}</a>"
        for uid, name in session["players"].items()
    )

    text = (
        f"🎮 Mafia o‘yini boshlandi! Tugmani bosib qo‘shiling:\n\n"
        f"👥 <b>Ro‘yxat:</b> {players_html}\n"
        f"🔢 <b>Jami:</b> {len(session['players'])} ta"
    )

    try:
        await call.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=join_game_keyboard()
        )
    except MessageNotModified:
        pass

# Ro'yxatdan o'tkazish
def register_join_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(join_game_callback, lambda c: c.data == "join_game")
