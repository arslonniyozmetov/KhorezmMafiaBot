from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("game", "🎮 Yangi o‘yin yaratish"),
        types.BotCommand("startgame", "🚀 O‘yinni boshlash"),
        types.BotCommand("leave", "🚪 O‘yindan chiqish"),
    ])
