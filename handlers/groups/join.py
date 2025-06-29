# handlers/groups/join.py
from aiogram import types
from aiogram.dispatcher import Dispatcher
from loader import dp
from utils.misc.session import get_session
from keyboards.inline.join_game import join_game_keyboard

@dp.callback_query_handler(lambda c: c.data == "join_game", chat_type=["group", "supergroup"])
async def join_game(call: types.CallbackQuery):
    user = call.from_user
    session = get_session(call.message.chat.id)

    if session["game_started"]:
        return await call.answer("O'yin allaqachon boshlangan.", show_alert=True)

    if user.id in session["players"]:
        return await call.answer("Siz allaqachon o'yindasiz.", show_alert=True)

    session["players"].append(user.id)
    await call.answer("O‘yinga qo‘shildingiz!")
    await call.message.edit_text(
        f"🎮 O‘yinga quyidagi o‘yinchilar qo‘shilmoqda: {len(session['players'])} ta\n"
        f"⏳ Yana o‘yinchilar qo‘shilishi mumkin.",
        reply_markup=join_game_keyboard()
    )
