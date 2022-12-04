from ..bot import bot,dp
from ..keyboards import Keyboards_admin
from aiogram.types import Message
kbd = Keyboards_admin()


@dp.callback_query_handler(text='add_user')
async def admin_settings(message: Message):
    """main btn what returns kbd w/ admin config"""
    mes_id = message['message']['message_id']
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text=f'You are in stage to add/delete or get list of admins.',
        reply_markup=kbd.main_menu()
    )
