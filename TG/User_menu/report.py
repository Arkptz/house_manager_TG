from ..bot import bot, dp
from ..keyboards import Keyboards_User
from ..states import Report
from ..decors import user
from ..houses_and_roles import get_house_list, roles
from Api.http_api import http
from Utility.classes import UserInfo, TempData
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from datetime import datetime
import asyncio
import re
kbd = Keyboards_User()
tmp: dict[int, TempData] = {}


async def send_report(user_id, house, edit=True, msg: Message = None):
    txt = 'Отчёт:\n'
    cur_report = await http.get_report_with_current_date(user_id, house)
    for task in cur_report.keys():
        ans = cur_report[task]
        ans = ans if ans != 'None' else '✅Всё гуд'
        txt += f'   {task}: {ans}\n'
    if edit:
        await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text=txt, reply_markup=kbd.tasks_kbd(tmp[user_id].tasks, cur_report, page=tmp[user_id].page))
    else:
        await bot.send_message(chat_id=user_id, text=txt, reply_markup=kbd.tasks_kbd(tmp[user_id].tasks, cur_report))
    await Report.tasks.set()


@dp.callback_query_handler(Text(startswith='select_house_'))
@user
async def add_report(cq: CallbackQuery):
    msg = cq.message
    user_id = msg.chat.id
    house = cq.data.split('select_house_')[1]
    tasks = await http.get_name_cols_for_table(name_table=house)
    tmp[user_id] = TempData(house, tasks)
    await send_report(user_id, house, msg=msg)


@dp.callback_query_handler(Text(startswith='select_role_'))
@user
async def select_role(cq: CallbackQuery):
    msg = cq.message
    user_id = msg.chat.id
    role = cq.data.split('select_role_')[1]
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выбери здание:', reply_markup=kbd.main_menu(role_user=role)[0])


@dp.callback_query_handler(Text(startswith='approve_task_'), state=Report.tasks)
@user
async def approve_task(cq: CallbackQuery, state: FSMContext):
    task = cq.data.split('approve_task_')[1]
    msg = cq.message
    user_id = msg.chat.id
    await http.update_report(user_id, tmp[user_id].name_table,  tasks={task: 'None'})
    await send_report(user_id, tmp[user_id].name_table, msg=msg)


@dp.callback_query_handler(Text(startswith='add_comment_'), state=Report.tasks)
@user
async def add_comment_(cq: CallbackQuery, state: FSMContext):
    task = cq.data.split('add_comment_')[1]
    msg = cq.message
    user_id = msg.chat.id
    await state.update_data(task=task)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text=f'Введи новый комментарий, для пункта "{task}":')
    await Report.comment.set()


@dp.message_handler(state=Report.comment)
@user
async def comment_input(msg: Message, state: FSMContext):
    data = await state.get_data()
    task = data['task']
    user_id = msg.chat.id
    await http.update_report(user_id, tmp[user_id].name_table, tasks={task: msg.text})
    await send_report(user_id, tmp[user_id].name_table, edit=False)


@dp.callback_query_handler(Text(startswith='replace_page_'), state=Report.tasks)
@user
async def replace_page(cq: CallbackQuery, state: FSMContext):
    page = int(cq.data.split('replace_page_')[1])
    msg = cq.message
    user_id = msg.chat.id
    tmp[user_id].page = page
    cur_report = await http.get_report_with_current_date(user_id, tmp[user_id].name_table)
    await bot.edit_message_reply_markup(user_id, message_id=msg.message_id, reply_markup=kbd.tasks_kbd(tmp[user_id].tasks, cur_report, page=page))
