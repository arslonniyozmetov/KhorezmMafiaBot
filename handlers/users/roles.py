from aiogram import Dispatcher, types
from utils.misc.session import get_session

# ==== DON ====
async def don_action(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    session = get_session(call.message.chat.id)
    session["night_actions"]["don"] = target_id
    await call.message.edit_text("🔫 Don o‘ljani tanladi!")

# ==== DOK ====
async def dok_action(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    session = get_session(call.message.chat.id)
    session["night_actions"]["dok"] = target_id
    await call.message.edit_text("💉 Dok davolashga tayyor!")

# ==== KOMISSAR tanlovi: tekshir/adash ====
async def komissar_decide(call: types.CallbackQuery):
    action = call.data.split(":")[1]
    session = get_session(call.message.chat.id)
    uid = str(call.from_user.id)
    session["night_actions"]["komissar_action"] = action
    session["night_actions"]["komissar"] = None
    await call.message.edit_text(f"🕵 Komissar: {action} ni tanladi.")
    from keyboards.inline.role_choices import player_choice_keyboard
    await call.bot.send_message(uid, "🎯 Nishonni tanlang:", reply_markup=player_choice_keyboard("komissar_target", session["players"], uid))

# ==== KOMISSAR kimga nisbatan ====
async def komissar_target(call: types.CallbackQuery):
    _, target_id = call.data.split(":")
    session = get_session(call.message.chat.id)
    session["night_actions"]["komissar"] = target_id
    await call.message.edit_text("🎯 Nishon qabul qilindi.")

# ==== Ro‘yxatdan o‘tkazish ====
def register_role_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(don_action, lambda c: c.data.startswith("don:"))
    dp.register_callback_query_handler(dok_action, lambda c: c.data.startswith("dok:"))
    dp.register_callback_query_handler(komissar_decide, lambda c: c.data.startswith("komissar:"))
    dp.register_callback_query_handler(komissar_target, lambda c: c.data.startswith("komissar_target:"))
