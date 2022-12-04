import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])


admin_list = ['1021524873']
BOT_TOKEN = '5334439271:AAFWmpskZqlpS35ezK99bWEeEI8NLV5SEZQ'
db_path = f'{homeDir}\\db.db'
host_url = '127.0.0.1'
port = 8000





