from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from Api.http_api import http
from .bot import bot


def admin(input_func):
    async def output_func(*args, **kwargs):
        msg = args[0]
        if type(msg) != Message:
            msg = msg.message  # каллбек
        if msg.chat.id in [i.id for i in await http.get_admins()]:
            try:
                await input_func(*args)
            except:
                await input_func(state=kwargs['state'], *args)

        else:
            await bot.send_message(msg.chat.id, 'Ты не админ.')
    return output_func


def user(input_func):
    async def output_func(*args, **kwargs):
        msg = args[0]
        if type(msg) != Message:
            msg = msg.message  # каллбек
        if msg.chat.id in [i.id for i in await http.get_all_users()]:
            try:
                await input_func(*args)
            except:
                await input_func(state=kwargs['state'], *args)
    return output_func
