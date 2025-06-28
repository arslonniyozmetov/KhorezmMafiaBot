from aiogram import Dispatcher, types
from utils.misc.session import get_session


async def join_game_callback(call: types.CallbackQuery):
    session = get_session(call.message.chat.id)
    user = call.from_user

    if not session or session["started"]:
        return await call.answer("O‘yin allaqachon boshlangan yoki mavjud emas.")

    if str(user.id) in session["players"]:
        return await call.answer("Siz allaqachon o‘yinga qo‘shilgansiz.")

    session["players"][str(user.id)] = user.full_name
    await call.answer("✅ O‘yinga qo‘shildingiz!")
    await call.message.edit_reply_markup(call.message.reply_markup)  # optional refresh


def register_join_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(join_game_callback, lambda c: c.data == "join_game")
