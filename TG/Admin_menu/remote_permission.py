from ..bot import bot, dp
from ..keyboards import Keyboards_admin
from ..states import AdminRemotePermission
from ..decors import admin
from Api.http_api import http
from Utility.classes import UserInfo
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import asyncio
kbd = Keyboards_admin()


@dp.callback_query_handler(text='admin_remote_permession')
@admin
async def add_admin(cq: CallbackQuery):
    msg = cq.message
    users = await http.get_all_users()
    kbd.users = users
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Выберите пользователя:', reply_markup=kbd.generate_page_users_with_filter())
    await AdminRemotePermission.user.set()


@dp.callback_query_handler(Text(startswith='select_user_'), state=AdminRemotePermission.user)
@admin
async def select_user(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    id = int(cq.data.split('select_user_')[1])
    user = await http.get_user(id)
    await state.update_data(user_id=id)
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f'Настройте права пользователя {user.name}:', reply_markup=kbd.roles_user(user))


@dp.callback_query_handler(Text(startswith='replace_page_'), state=AdminRemotePermission.user)
@admin
async def replace_page(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    page = int(cq.data.split('replace_page_')[1])
    data = await state.get_data()
    if 'filters' in data:
        filters = data['filters']
    else:
        filters = ''
    await bot.edit_message_reply_markup(chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=kbd.generate_page_users_with_filter(page=page, filters=filters))


@dp.callback_query_handler(Text(startswith='set_filter_'), state=AdminRemotePermission.user)
@admin
async def set_filter_(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    filters = cq.data.split('set_filter_')[1]
    await state.update_data(filters=filters)
    await bot.edit_message_reply_markup(chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=kbd.generate_page_users_with_filter(filters=filters))


@dp.callback_query_handler(Text(startswith="give_role_"), state=AdminRemotePermission.user)
@admin
async def give_role(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    role = cq.data.split('give_role_')[1]
    data = await state.get_data()
    user = user = await http.get_user(data['user_id'])
    if getattr(user, role):
        setattr(user, role, False)
    else:
        setattr(user, role, True)
    await http.update_user(user.__dict__)
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f'Пользователю {user.name} выдана роль: {role}', reply_markup=kbd.roles_user(user))


@dp.callback_query_handler(text="delete_user", state=AdminRemotePermission.user)
@admin
async def delete_user(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    data = await state.get_data()
    await http.delete_user(data['user_id'])
    await state.finish()
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Админ меню:', reply_markup=kbd.main_menu())
