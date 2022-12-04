from ..bot import bot, dp
from ..keyboards import Keyboards_admin
from ..states import AdminAddUser
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
kbd = Keyboards_admin()


@dp.callback_query_handler(text='admin_add_user')
async def admin_settings(cq: CallbackQuery):
    msg = cq.message
    """main btn what returns kbd w/ admin config"""
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='Введите имя пользователя:')
    await AdminAddUser.name.set()

@dp.message_handler(state=AdminAddUser.name)
async def input_name(msg:Message, state:FSMContext):
    await state.update_data(name = msg.text)
    await bot.send_message(msg.chat.id, 'Введите id пользователя:')
    await AdminAddUser.next()

@dp.message_handler(state=AdminAddUser.id)
async def input_id(msg:Message, state:FSMContext):
    try:
        id = int(msg.text)
    except:
        await bot.send_message(msg.chat.id, 'Неверный формат.')

    await state.update_data(id = msg.text)
    await bot.send_message(msg.chat.id, 'Выдать пользователю админа?', reply_markup=kbd.give_admin())
    await AdminAddUser.next()

@dp.callback_query_handler(Text(startswith="button_submit_"), state = AdminAddUser.admin)
async def input_admin(cq: CallbackQuery, state:FSMContext):
    msg = cq.message
    data = cq.data.split('button_submit_')[1]
    admin = True if data =='yes' else False
    await state.update_data(admin=admin)
    """main btn what returns kbd w/ admin config"""
    await state.finish()
    data = await state.get_data()
    

