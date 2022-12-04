from dataclasses import dataclass
from aiogram import Bot, Dispatcher, executor


@dataclass
class ConfigClass:
    admin_list:list
    bot_token:str
    db_path:str
    host_url:str
    port:int
    dp:Dispatcher=None
    bot:Bot=None

class BotVariables:
    bot:Bot = None
    dp:Dispatcher = None