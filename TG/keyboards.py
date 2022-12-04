from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



class Keyboards_User:

    def __init__(self):
        self.btn_back_to_menu = InlineKeyboardButton(
            text='↩️Back to menu',
            callback_data='back_to_menu'
        )


class Keyboards_admin():
    def __init__(self):
        self.btn_back_to_menu = InlineKeyboardButton(
            text='↩️Back to menu',
            callback_data='back_to_menu'
        )
    def main_menu(self):
        markup = InlineKeyboardMarkup(row_width=2)
        add_user = InlineKeyboardButton(text='Добавить пользователя', callback_data='admin_add_user')
        add_admin = InlineKeyboardButton(text='Добавить админа', callback_data='admin_add_admin')
        remove_admin = InlineKeyboardButton(text='Удалить админа', callback_data='admin_delete_admin')
        add_permission = InlineKeyboardButton(text='Выдать права пользователю', callback_data='admin_give_permission')
        delete_permission = InlineKeyboardButton(text='Забрать права у пользователя', callback_data='admin_delete_permission')
        markup.add(add_user, add_admin, remove_admin, add_permission, delete_permission)
        return markup
    def give_admin(self):
        markup = InlineKeyboardMarkup(row_width=2)
        yes = InlineKeyboardButton(text='Да',callback_data= 'button_submit_yes')
        no = InlineKeyboardButton(text='Нет',callback_data= 'button_submit_no')
        markup.add(yes, no,)
        return markup

