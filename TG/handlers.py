from .keyboards import Keyboards_admin
from Api.http_api import http
from .bot import dp, bot
from loguru import logger as log
from . import Admin_menu
import sqlite3
import config as cfg
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from .states import AdminAddAdmin, AdminAddUser,AdminDeleteAdmin, AdminRemotePermission
kbd = Keyboards_admin()



async def on_startup(dp):
    """ try to add admins and create table to add MAIN admin from cfg.admin_list"""
    await http.add_admins(list_admins=cfg.admin_list)
    """ notify admins when bot started """
    log.info('send main menu')

    admins_list = [admin.id for admin in await http.get_admins()]
    for admin in admins_list:
        menu_markup = kbd.main_menu()
        await bot.send_message(
            chat_id=admin,
            text='<b>Бот запущен.</b>',
            reply_markup=menu_markup
        )

@dp.message_handler(commands=['start', 'menu'])
async def start(msg: Message):
    menu_markup = kbd.main_menu()
    await bot.send_message(
        chat_id=msg.chat.id,
        text='<b>Админ меню:</b>',
        reply_markup=menu_markup
    )

@dp.callback_query_handler(text='back_to_menu', state=[AdminAddUser.permission,AdminAddUser.name, AdminAddUser.id, AdminRemotePermission.id,])
async def back_to_menu(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    menu_markup = kbd.main_menu()
    await bot.edit_message_text(
        chat_id=msg.chat.id, message_id=msg.message_id,
        text='<b>Админ меню:</b>',
        reply_markup=menu_markup
    )
    await state.finish()