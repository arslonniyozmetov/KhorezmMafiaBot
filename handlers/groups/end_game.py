# handlers/groups/end_game.py
from aiogram import types
from loader import dp
from handlers.game.end_game import check_win_conditions

@dp.message_handler(commands=["endgame"], chat_type=["group", "supergroup"])
async def end_game(message: types.Message):
    result = check_win_conditions(message.chat.id)
    if result:
        await message.answer(f"🏁 O‘yin tugadi!\n\n{result}")
    else:
        await message.answer("⏳ O‘yin hali tugamagan.")
