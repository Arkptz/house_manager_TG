from ..bot import bot, dp
from ..keyboards import Keyboards_admin
from ..states import AdminRemotePermission
from Api.http_api import http
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
    await AdminRemotePermission.id.set()


@dp.callback_query_handler(Text(startswith='select_user_'), state=AdminRemotePermission.id)
async def select_user(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    id = int(cq.data.split('select_user_')[1])
    await http.add_admins([id])
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Админ права выданы', reply_markup=kbd.main_menu())
    await state.finish()


@dp.callback_query_handler(Text(startswith='replace_page_'), state=AdminRemotePermission.id)
async def replace_page(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    page = int(cq.data.split('replace_page_')[1])
    await bot.edit_message_reply_markup(chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=kbd.generate_page_users_with_filter(page=page))


@dp.callback_query_handler(Text(startswith='set_filter_'), state=AdminRemotePermission.id)
async def set_filter_(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    kbd.filters = cq.data.split('set_filter_')[1]
    await bot.edit_message_reply_markup(chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=kbd.generate_page_users_with_filter())
