
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from ..bot import bot, dp
from ..keyboards import Keyboards_admin
from ..states import AdminAddUser
from Api.http_api import http
from Utility.classes import UserInfo


kbd = Keyboards_admin()


@dp.callback_query_handler(text='admin_add_user')
async def admin_settings(cq: CallbackQuery):
    msg = cq.message
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Введите имя пользователя:', reply_markup=kbd.back_markup())
    await AdminAddUser.name.set()


@dp.message_handler(state=AdminAddUser.name)
async def input_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await bot.send_message(msg.chat.id, 'Введите id пользователя:', reply_markup=kbd.back_markup())
    await AdminAddUser.next()


@dp.message_handler(state=AdminAddUser.id)
async def input_id(msg: Message, state: FSMContext):
    try:
        id = int(msg.text)
    except:
        await bot.send_message(msg.chat.id, 'Неверный формат.')
        return ''

    await state.update_data(id=msg.text)
    kbd.roles = await http.get_columns_names()
    await bot.send_message(msg.chat.id, 'Какую роль выдать пользователю?', reply_markup=kbd.give_role())
    await AdminAddUser.next()


@dp.callback_query_handler(Text(startswith="give_role_"), state=AdminAddUser.permission)
async def input_admin(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    role = cq.data.split('give_role_')[1]
    data = await state.get_data()
    user = UserInfo(data['name'], data['id'])
    setattr(user, role, True)
    await http.add_user(user.__dict__)
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f'Пользователь {user.name} добавлен', reply_markup=kbd.main_menu())
    await state.finish()
