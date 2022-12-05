from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Utility.classes import UserInfo
from Api.http_api import http
from config import count_buttons_for_one_page as cbfop, count_tasks_for_one_page as ctfop
from .houses_and_roles import houses as hs, roles as rl


class Keyboards_User:
    houses = hs
    roles = rl
    tasks:list
    name_table:str
    def __init__(self):
        self.btn_back_to_menu = InlineKeyboardButton(
            text='↩️Вернуться в меню',
            callback_data='back_to_menu'
        )

    def main_menu(self, user: UserInfo):
        markup = InlineKeyboardMarkup(row_width=3)
        for role in self.roles:
            if getattr(user, role):
                role_user = role
        for house in self.houses:
            if role_user in house:
                name_house = house.replace(f'_{role_user}', '')
                markup.insert(InlineKeyboardButton(text=name_house,
                                                   callback_data=f'select_house_{house}'))
        return markup
    

    def tasks_kbd(self,current_report:dict[str, str], page=0):
        markup = InlineKeyboardMarkup(row_width=3)
        start = page *ctfop
        select_tasks = self.tasks[start:start+ctfop]
        for task in select_tasks:
            lst_buttons = []
            task_res = current_report[task]
            if task_res != '':
                lst_buttons.append(InlineKeyboardButton(text=f'✅{task}', callback_data='////'))
                if task_res == 'None':
                    lst_buttons.append(InlineKeyboardButton(text='📝(Доб. комм.)', callback_data=f'add_comment_{task}'))
                else:
                    lst_buttons.append(InlineKeyboardButton(text='📝(Изм. комм.)', callback_data=f'add_comment_{task}'))
            else:
                lst_buttons.append(InlineKeyboardButton(text=task, callback_data='////'))
                lst_buttons.append(InlineKeyboardButton(text='✅(Всё гуд)', callback_data=f'approve_task_{task}'))
                lst_buttons.append(InlineKeyboardButton(text='📝(Доб. комм.)', callback_data=f'add_comment_{task}'))
            markup.row(*lst_buttons)
        markup.row(InlineKeyboardButton(
            text='------------------------------------------', callback_data='.....'))
        footer = []
        if page != 0:
            footer.append(InlineKeyboardButton(
                text='⬅️Предыдущая страница', callback_data=f'replace_page_{page-1}'))
        footer.append(InlineKeyboardButton(
            text=f'Стр. №{page+1}', callback_data=f'{page}'))
        footer.append(InlineKeyboardButton(
            text='➡️Следующая страница', callback_data=f'replace_page_{page+1}'))
        markup.row(*footer)
        markup.row(self.btn_back_to_menu)
        return markup


class Keyboards_admin():
    users: list[UserInfo]
    roles = rl
    filters: str = ''

    def __init__(self):
        self.btn_back_to_menu = InlineKeyboardButton(
            text='↩️Вернуться в меню',
            callback_data='back_to_menu'
        )

    def back_markup(self,):
        markup = InlineKeyboardMarkup()
        markup.row(self.btn_back_to_menu)
        return markup

    def main_menu(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=3)
        add_user = InlineKeyboardButton(
            text='Добавить пользователя', callback_data='admin_add_user')
        add_permission = InlineKeyboardButton(
            text='Управление правами пользователей', callback_data='admin_remote_permession')
        # add_admin = InlineKeyboardButton(
        #     text='Добавить админа', callback_data='admin_add_admin')
        # remove_admin = InlineKeyboardButton(
        #     text='Удалить админа', callback_data='admin_delete_admin')
        # add_permission = InlineKeyboardButton(
        #     text='Выдать права пользователю', callback_data='admin_give_permission')
        # delete_permission = InlineKeyboardButton(
        #     text='Забрать права у пользователя', callback_data='admin_delete_permission')
        # markup.add(add_user, add_admin, remove_admin,
        #            add_permission, delete_permission)
        markup.add(add_user, add_permission)
        markup.row(InlineKeyboardButton(
            'Добавить новый дом', callback_data='add_new_house'))
        return markup

    def give_admin(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=2)
        yes = InlineKeyboardButton(
            text='Да', callback_data='button_submit_yes')
        no = InlineKeyboardButton(text='Нет', callback_data='button_submit_no')
        markup.add(yes, no,)
        markup.row(self.btn_back_to_menu)
        return markup

    def _filter_users(self,) -> list[UserInfo]:
        new_list = []
        for user in self.users:
            for role in self.roles:
                if self.filters == role and getattr(user, role):
                    new_list.append(user)
        return new_list

    def generate_page_users_with_filter(self, page=0) -> InlineKeyboardMarkup:
        start = page * cbfop
        users = self.users
        if self.filters != '':
            users = self._filter_users()

        select_users = users[start: start + cbfop]
        markup = InlineKeyboardMarkup()

        list_filters = []
        for i in self.roles:
            list_filters.append(InlineKeyboardButton(
                text=('🟢' if self.filters == i else '') + i, callback_data=f'set_filter_{i}'))
        _slice = len(list_filters) // 2
        markup.row(InlineKeyboardButton(text='♻️Фильтр',
                   callback_data='set_filter_'), *list_filters[:_slice])
        markup.row(*list_filters[_slice:])
        markup.row(InlineKeyboardButton(
            text='------------------------------------------', callback_data='.....'))
        markup.row(InlineKeyboardButton(text="👀Юзеры:", callback_data='users'))

        for i in range(0, len(select_users), 2):
            us_1_2 = select_users[i:i+2]
            if len(us_1_2) == 2:
                user1, user2 = us_1_2
                markup.row(InlineKeyboardButton(text=f'{user1.name} (id: {user1.id})',
                                                callback_data=f'select_user_{user1.id}'),
                           InlineKeyboardButton(text=f'{user2.name} (id: {user2.id})',
                                                callback_data=f'select_user_{user2.id}'))
            else:
                user1 = us_1_2[0]
                markup.row(InlineKeyboardButton(text=f'{user1.name} (id: {user1.id})',
                                                callback_data=f'select_user_{user1.id}'))
        markup.row(InlineKeyboardButton(
            text='------------------------------------------', callback_data='.....'))
        footer = []
        if page != 0:
            footer.append(InlineKeyboardButton(
                text='⬅️Предыдущая страница', callback_data=f'replace_page_{page-1}'))
        footer.append(InlineKeyboardButton(
            text=f'Стр. №{page+1}', callback_data=f'{page}'))
        footer.append(InlineKeyboardButton(
            text='➡️Следующая страница', callback_data=f'replace_page_{page+1}'))
        markup.row(*footer)
        markup.row(self.btn_back_to_menu)
        return markup

    def give_role(self):
        lenght = ln = len(self.roles)
        rw = ln//2 if ln % 2 == 0 else ln//2 + 1
        markup = InlineKeyboardMarkup(row_width=rw)
        for role in self.roles:
            markup.insert(InlineKeyboardButton(
                text=role, callback_data=f'give_role_{role}'))
        return markup

    def roles_user(self, user: UserInfo):
        lenght = ln = len(self.roles)
        rw = ln//2 if ln % 2 == 0 else ln//2 + 1
        markup = InlineKeyboardMarkup(row_width=rw)
        for role in self.roles:
            val = getattr(user, role)
            markup.insert(InlineKeyboardButton(
                text=('🟢' if val else '') + role, callback_data=f'give_role_{role}'))

        markup.row(InlineKeyboardButton(
            text='❌Удалить пользователя', callback_data='delete_user'))
        markup.row(self.btn_back_to_menu)
        return markup

    def approve_house(self, ):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(
            text='✅Подтвердить', callback_data='add_house_approve'))
        markup.insert(InlineKeyboardButton(
            text='🛠Изменить пункты проверок', callback_data='add_house_replace'))

        markup.row(self.btn_back_to_menu)
        return markup
