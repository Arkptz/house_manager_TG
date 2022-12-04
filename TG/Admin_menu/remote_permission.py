from ..bot import bot, dp
from ..keyboards import Keyboards_admin
from ..states import AdminRemotePermission
from Api.http_api import http
from Utility.classes import UserInfo
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import asyncio
kbd = Keyboards_admin()


@dp.callback_query_handler(text='admin_remote_permession')
async def add_admin(cq: CallbackQuery):
    msg = cq.message
    users = await http.get_all_users()
    kbd.filters = ''
    kbd.users = users
    kbd.roles = await http.get_columns_names()
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Выберите пользователя:', reply_markup=kbd.generate_page_users_with_filter())
    await AdminRemotePermission.user.set()


@dp.callback_query_handler(Text(startswith='select_user_'), state=AdminRemotePermission.user)
async def select_user(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    id = int(cq.data.split('select_user_')[1])
    user = await http.get_user(id)
    await state.update_data(name=user.name, id=id)
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f'Настройте права пользователя {user.name}:', reply_markup=kbd.roles_user(user))


@dp.callback_query_handler(Text(startswith='replace_page_'), state=AdminRemotePermission.user)
async def replace_page(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    page = int(cq.data.split('replace_page_')[1])
    await bot.edit_message_reply_markup(chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=kbd.generate_page_users_with_filter(page=page))


@dp.callback_query_handler(Text(startswith='set_filter_'), state=AdminRemotePermission.user)
async def set_filter_(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    kbd.filters = cq.data.split('set_filter_')[1]
    await bot.edit_message_reply_markup(chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=kbd.generate_page_users_with_filter())


@dp.callback_query_handler(Text(startswith="give_role_"), state=AdminRemotePermission.user)
async def give_role(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    role = cq.data.split('give_role_')[1]
    data = await state.get_data()
    user = UserInfo(data['name'], data['id'])
    setattr(user, role, True)
    await http.update_user(user.__dict__)
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f'Пользователю {user.name} выдана роль: {role}', reply_markup=kbd.roles_user(user))


@dp.callback_query_handler(text="delete_user", state=AdminRemotePermission.user)
async def delete_user(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    data = await state.get_data()
    await http.delete_user(data['id'])
    await state.finish()
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f'Админ меню:', reply_markup=kbd.main_menu())
