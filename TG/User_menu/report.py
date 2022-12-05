from ..bot import bot, dp
from ..keyboards import Keyboards_User
from ..states import Report
from ..houses_and_roles import houses, roles
from Api.http_api import http
from Utility.classes import UserInfo, TempData
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from datetime import datetime
import asyncio
import re
kbd = Keyboards_User()


@dp.callback_query_handler(text='select_house_')
async def add_house(cq: CallbackQuery):
    msg = cq.message
    user_id = msg.chat.id
    house = cq.data.split('select_house_')[1]
    cur_report = await http.get_report_with_current_date(user_id, house)
    kbd.tasks = await http.get_name_cols_for_table(name_table=house)
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Создание отчёта:\n', reply_markup=kbd.back_markup())
    await Report.tasks.set()


@dp.callback_query_handler(text='select_house_', state=Report.house)
async def input_name(msg: Message, state: FSMContext):
    ans = re.findall('^[А-Яа-яA-Za-z0-9_-]{3,50}$', msg.text)
    if not ans:
        await bot.send_message(chat_id=msg.chat.id,
                               text='Неверный формат', reply_markup=kbd.back_markup())
