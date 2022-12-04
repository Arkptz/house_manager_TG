import os
from Parts.classes import ConfigClass
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])


admin_list = ['1021524873']
BOT_TOKEN = '5334439271:AAFWmpskZqlpS35ezK99bWEeEI8NLV5SEZQ'
db_path = f'{homeDir}\\db.db'
host_url = '127.0.0.1'
port = 8000




cf = ConfigClass(admin_list=admin_list, bot_token=BOT_TOKEN, db_path=db_path, host_url=host_url, port=port)
storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(cf.bot_token, parse_mode='HTML', disable_web_page_preview=True)
dp = Dispatcher(bot, storage=storage, loop=loop)
cf.dp = dp
cf.bot = bot

