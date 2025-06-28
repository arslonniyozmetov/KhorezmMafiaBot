from aiogram import Bot
from aiogram.types import BotCommand

async def set_default_commands(bot: Bot):
    commands = [
        BotCommand("start", "Botni ishga tushurish"),
        BotCommand("game", "Yangi o‘yinni boshlash"),
        BotCommand("vote", "Ovoz berishni boshlash"),
        BotCommand("cancel", "O‘yinni bekor qilish"),
        BotCommand("players", "O‘yinchilar ro‘yxati"),
        BotCommand("status", "O‘yin holatini ko‘rish"),
    ]
    await bot.set_my_commands(commands)
