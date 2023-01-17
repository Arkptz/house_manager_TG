import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])


admin_list = [['\_-_/',1021524873],['Ilya Ermi',828458879]] #[name,id]
BOT_TOKEN = '5849628959:AAHXJAHn63SjKVCVbnNIajGDauoDOFitrQw'
USER_BOT_TOKEN = '5772331354:AAFvlbXM19WqsfhTv2qCLY5ur7V8EBEuZ2s' #@testim_bbbbot
host_webapps = 'https://prostorstroj.ru'
db_path = f'{homeDir}\\db.db'
host_url = '0.0.0.0'
port = 8001
count_buttons_for_one_page = 20 #юзеры/админ панель
count_tasks_for_one_page = 10 #таски/юезр панель
