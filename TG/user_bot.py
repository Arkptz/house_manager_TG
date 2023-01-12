# import asyncio

# from aiogram import Bot, Dispatcher, executor
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from config import USER_BOT_TOKEN
# from aiogram.types import Message
# from aiogram.types import Message
# from aiogram.dispatcher import FSMContext
# from aiogram.types import Message, CallbackQuery
# from Api.http_api import http
# from .decors import user
# from .keyboards import Keyboards_User
# from .states import AdminAddAdmin, AdminAddUser, AdminDeleteAdmin, AdminRemotePermission, AddHouse, Report

# kbd = Keyboards_User()

# storage = MemoryStorage()
# loop = asyncio.get_event_loop()
# bot = Bot(USER_BOT_TOKEN, parse_mode='HTML', disable_web_page_preview=True)
# dp = Dispatcher(bot, storage=storage, loop=loop)


# @dp.message_handler(commands=['user'])
# @user
# async def user_menu(msg: Message):
#     user_id = msg.chat.id
#     user = await http.get_user(user_id)
#     menu_markup = kbd.main_menu(user)
#     txt = 'Выбери здание' if menu_markup[1] == 'houses' else 'Выбери проффесию'
#     await bot.send_message(
#         chat_id=msg.chat.id,
#         text=f'<b>{txt}:</b>',
#         reply_markup=menu_markup[0]
#     )

# @dp.callback_query_handler(text='back_to_menu',
#                            state=[AdminAddUser.permission,
#                                   AdminAddUser.name,
#                                   AdminAddUser.id,
#                                   AdminRemotePermission.user,
#                                   AddHouse.name,
#                                   AddHouse.role,
#                                   AddHouse.args_list, AddHouse.approve,
#                                   Report.tasks])
# @user
# async def back_to_menu(cq: CallbackQuery, state: FSMContext):
#     msg = cq.message
#     user_id = msg.chat.id
#     _user = await http.get_user(user_id)
#     menu_markup = kbd.main_menu(_user)
#     await bot.edit_message_text(
#         chat_id=msg.chat.id, message_id=msg.message_id,
#         text='<b>Выбери здание:</b>',
#         reply_markup=menu_markup[0]
#     )
#     await state.finish()

# dp.register_callback_query_handler(back_to_menu, text='back_to_menu',)


# def start_bot():
#     executor.start_polling(dp)
