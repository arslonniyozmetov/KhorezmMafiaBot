from aiogram import executor

from loader import dp, bot  # bot ni qo‘shamiz!
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from handlers import register_all_handlers


async def on_startup(dispatcher):
    # ✅ BOT obyekt yuboriladi
    await set_default_commands(bot)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    register_all_handlers(dp)
    executor.start_polling(dp, on_startup=on_startup)
