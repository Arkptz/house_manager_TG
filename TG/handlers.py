from .keyboards import Keyboards_admin
from Api.http_api import http
from .bot import dp, bot
from loguru import logger as log
import sqlite3
import config as cfg

kbd = Keyboards_admin()

async def on_startup(dp):
    """ try to add admins and create table to add MAIN admin from cfg.admin_list"""
        await http.add_admins(id_list=cfg.admin_list)
    """ notify admins when bot started """
    log.info('send main menu')

    admins_list = [admin.id for admin in await http.get_admins()]
    for admin in admins_list:
        menu_markup = kbd.main_menu()
        await bot.send_message(
            chat_id=admin,
            text='<b>Bot launched.</b>',
            reply_markup=menu_markup
        )