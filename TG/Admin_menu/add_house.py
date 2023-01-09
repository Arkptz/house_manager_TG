from ..bot import bot, dp
from ..keyboards import Keyboards_admin
from ..states import AddHouse
from ..houses_and_roles import get_house_list, roles
from ..decors import admin
from config import host_webapps
from aiogram.types import WebAppInfo
from Api.http_api import http
from Utility.classes import UserInfo, TempData
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import asyncio
import re
kbd = Keyboards_admin()


@dp.message_handler(content_types=['web_app_data'])
async def test(*args):
    print(args)


@dp.callback_query_handler(text='add_new_house')
@admin
async def add_house(cq: CallbackQuery):
    msg = cq.message
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Введите уникальное название дома (без пробелов):\n'
                                                                                     'Допустимые символы: А-Я, а-я, A-Z, a-z, 0-9, _, -', reply_markup=kbd.back_markup())
    await AddHouse.name.set()


@dp.message_handler(state=AddHouse.name)
@admin
async def input_name(msg: Message, state: FSMContext):
    ans = re.findall('^[А-Яа-яA-Za-z0-9_-]{3,50}$', msg.text)
    if not ans:
        await bot.send_message(chat_id=msg.chat.id,
                               text='Неверный формат', reply_markup=kbd.back_markup())
        return ''
    await state.update_data(name=msg.text)
    await bot.send_message(msg.chat.id, text='Выберите профессию:', reply_markup=kbd.give_role())
    await AddHouse.next()


@dp.callback_query_handler(Text(startswith="give_role_"), state=AddHouse.role)
@admin
async def input_admin(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    role = cq.data.split('give_role_')[1]
    data = await state.get_data()
    await state.update_data(role=role)
    name_house = data['name']
    full_name_house = name_house + '_' + role
    if full_name_house in get_house_list():
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                    text='Такая конфигурация уже существует. Введите уникальное название дома:', reply_markup=kbd.back_markup())
        await AddHouse.name.set()
    else:
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                    text=f'Название дома: {name_house}\nПрофессия работника: {role}\n\n\n'
                                    'Введите все пункты проверок для работника, без пробелов, через запятую\n'
                                    'Допустимые символы: А-Я, а-я, A-Z, a-z, 0-9, _, -', reply_markup=kbd.back_markup())
        await AddHouse.next()


@dp.message_handler(state=AddHouse.args_list)
@admin
async def input_args(msg: Message, state: FSMContext):
    ans = re.findall(
        '^([А-Яа-яA-Za-z0-9_-]{2,50}\,){0,500}([А-Яа-яA-Za-z0-9_-]{1,50})$', msg.text)
    if not ans:
        await bot.send_message(chat_id=msg.chat.id,
                               text='Неверный формат', reply_markup=kbd.back_markup())
        return ''
    else:
        args_list = msg.text.split(',')
        await state.update_data(args_list=args_list)
        data = await state.get_data()
        _str = f"Подверди конфигурацию:\n\nНазвание дома: {data['name']}\nПрофессия работника:{data['role']}\n\nПроверки:\n"
        for num, check in enumerate(args_list):
            _str += f'  {num+1}) {check}\n'
        await bot.send_message(msg.chat.id, text=_str, reply_markup=kbd.approve_house())
        await AddHouse.next()


@dp.callback_query_handler(Text(startswith="add_house_"), state=AddHouse.approve)
@admin
async def approve(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    doing = cq.data.split('add_house_')[1]
    if doing == 'approve':
        data = await state.get_data()
        full_name_house = f'{data["name"]}_{data["role"]}'
        await http.create_new_table(name_table=full_name_house, args_list=data['args_list'])
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                    text='Дом был успешно добавлен.', reply_markup=kbd.back_markup())
    else:
        await AddHouse.args_list.set()
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                    text='Введите все пункты проверок для работника, без пробелов, через запятую\n'
                                    'Допустимые символы: А-Я, а-я, A-Z, a-z, 0-9, _, -', reply_markup=kbd.back_markup())
