from .keyboards import Keyboards_admin, Keyboards_User
from Api.http_api import http
from .bot import dp, bot
from .decors import admin, user
from Utility.classes import UserInfo
from loguru import logger as log
from . import Admin_menu
import sqlite3
import config as cfg
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from .states import AdminAddAdmin, AdminAddUser, AdminDeleteAdmin, AdminRemotePermission, AddHouse, Report
kbd_a = Keyboards_admin()
kbd = Keyboards_User()


async def on_startup(dp):
    """ try to add admins and create table to add MAIN admin from cfg.admin_list"""
    await http.add_admins(list_admins=[UserInfo(admin=True,*i).__dict__ for i in cfg.admin_list])
    """ notify admins when bot started """
    log.info('send main menu')

    admins_list = [admin.id for admin in await http.get_admins()]
    for _admin in admins_list:
        menu_markup = kbd_a.main_menu()
        try:
            await bot.send_message(
                chat_id=_admin,
                text='<b>Бот запущен.</b>',
                reply_markup=menu_markup
            )
        except:
            pass


@dp.message_handler(commands=['admin'])
@admin
async def admin_menu(msg: Message):
    user_id = msg.chat.id
    menu_markup = kbd_a.main_menu()
    await bot.send_message(
        chat_id=msg.chat.id,
        text='<b>Админ меню:</b>',
        reply_markup=menu_markup
    )


@dp.message_handler(commands=['user'])
@user
async def user_menu(msg: Message):
    user_id = msg.chat.id
    user = await http.get_user(user_id)
    menu_markup = kbd.main_menu(user)
    txt = 'Выбери здание' if menu_markup[1] == 'houses' else 'Выбери проффесию'
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f'<b>{txt}:</b>',
        reply_markup=menu_markup[0]
    )


@dp.callback_query_handler(text='back_to_menu',
                           state=[AdminAddUser.permission,
                                  AdminAddUser.name,
                                  AdminAddUser.id,
                                  AdminRemotePermission.user,
                                  AddHouse.name,
                                  AddHouse.role,
                                  AddHouse.args_list, AddHouse.approve,
                                  Report.tasks])
@user
async def back_to_menu(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    if user_id in [i.id for i in await http.get_admins()]:
        menu_markup = kbd_a.main_menu()
        await bot.edit_message_text(
            chat_id=msg.chat.id, message_id=msg.message_id,
            text='<b>Админ меню:</b>',
            reply_markup=menu_markup
        )
    else:
        user = await http.get_user(user_id)
        menu_markup = kbd.main_menu(user)
        await bot.edit_message_text(
            chat_id=msg.chat.id, message_id=msg.message_id,
            text='<b>Выбери здание:</b>',
            reply_markup=menu_markup
        )
    await state.finish()
