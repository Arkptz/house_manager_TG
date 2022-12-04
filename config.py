import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])


admin_list = ['1021524873']
BOT_TOKEN = '5849628959:AAHXJAHn63SjKVCVbnNIajGDauoDOFitrQw'
db_path = f'{homeDir}\\db.db'
host_url = '127.0.0.1'
port = 8000
count_buttons_for_one_page =20




