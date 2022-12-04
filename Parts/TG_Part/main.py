import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from classes import ConfigClass, BotVariables
from aiogram.types import Message

bv = BotVariables()
def start_bot(cf: ConfigClass):
    setattr(bv, 'bot', cf.bot)
    setattr(bv, 'dp', cf.dp)
    from . import dop_handler
    @cf.dp.message_handler(commands=['start'])
    async def test(msg:Message):
        await cf.bot.send_message(msg.chat.id, 'тест')

    executor.start_polling(cf.dp)
#lol