import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from aiogram.types import Message

storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML', disable_web_page_preview=True)
dp = Dispatcher(bot, storage=storage, loop=loop)


@dp.message_handler(commands=['start'])
async def test(msg: Message):
    await bot.send_message(msg.chat.id, 'тест')


def start_bot():
    from .handlers import dp, on_startup
    executor.start_polling(dp, on_startup=on_startup)
