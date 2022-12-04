from .main import bv
from aiogram.types import Message
dp = bv.dp
bot = bv.bot

@dp.message_handler(commands='test')
async def test(msg:Message):
    await bot.send_message(msg.chat.id, '////')