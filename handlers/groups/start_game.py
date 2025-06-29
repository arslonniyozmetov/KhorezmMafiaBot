from aiogram import types
from loader import dp, bot
from utils.misc.session import get_session, start_game
from handlers.roles.distributor import distribute_roles
from utils.helpers import send_pm
from handlers.game.night_circle import start_night_phase


@dp.message_handler(commands=["startgame"], chat_type=["group", "supergroup"])
async def start_game_handler(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    session = get_session(chat_id)

    if session["game_started"]:
        return await message.reply("⚠️ O‘yin allaqachon boshlangan.")

    # ✅ Admin yoki o‘yin yaratuvchisi bo‘lishi shart
    admins = await bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in admins]

    if user_id != session.get("host_id") and user_id not in admin_ids:
        return await message.reply("❌ Siz bu buyruqni bajarishga ruxsatsiz emas.")

    players = session.get("players", [])
    if len(players) < 4:
        return await message.reply("❗ Kamida 4ta o‘yinchi kerak.")

    start_game(chat_id)
    role_map = distribute_roles(players)
    session["roles"] = role_map

    failed = 0
    for pid in players:
        role = role_map[pid]
        try:
            await send_pm(pid, f"🎭 Sizning ro‘lingiz: <b>{role.name}</b>\n\n{role.description}")
        except:
            failed += 1
            await message.reply(f"⚠️ <a href='tg://user?id={pid}'>O‘yinchi</a>ga ro‘l yuborilmadi.", parse_mode="HTML")

    await message.reply(f"✅ O‘yin boshlandi! {len(players) - failed} ta o‘yinchiga ro‘l yuborildi.")
    await start_night_phase(chat_id)
