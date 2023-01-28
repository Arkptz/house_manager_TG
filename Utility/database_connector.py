import sqlite3 as sl
from config import db_path
from datetime import datetime
from typing import Union
import os


class UsersDatabaseConnector:
    """connector to database w/ users"""

    def __init__(self, connect: sl.Connection, cursor: sl.Cursor):
        self.db = connect
        self.cursor = cursor

    def create_table(self):
        """Creates table if not exists."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                                name TEXT,
                                id int,
                                admin BOOLEAN,
                                it BOOLEAN,
                                electrical BOOLEAN,
                                fireman BOOLEAN,
                                engineer BOOLEAN
                                )''')
        self.db.commit()

    def get_columns_names(self,) -> list[str]:
        cols = self.cursor.execute('''PRAGMA table_info(User) ''').fetchall()
        cols_res = []
        for i in cols:
            col_name = i[1]
            if not col_name in ['name', 'id']:
                cols_res.append(col_name)
        return cols_res

    async def get_admins(self,) -> list[tuple]:
        ans = self.cursor.execute('SELECT * FROM User WHERE admin').fetchall()
        return ans

    async def add_admins(self, list_users: list[dict]) -> None:
        for user in list_users:
            data = self.cursor.execute(
                'SELECT * FROM User WHERE id=?', [user['id']]).fetchall()
            if len(data) == 0:
                self.cursor.execute('INSERT INTO User VALUES(?,?,?,?,?,?,?)',
                                    list(user.values()))
            else:
                self.cursor.execute(
                    f'UPDATE User set admin = {True} WHERE id=?', [user['id']])
        self.db.commit()

    async def add_user(self, user_info: dict):
        self.cursor.execute('INSERT INTO User VALUES(?,?,?,?,?,?,?)',
                            list(user_info.values()))
        self.db.commit()

    async def delete_user(self, user_id: int):
        self.cursor.execute('DELETE FROM User WHERE id = ?', [user_id])
        self.db.commit()

    async def get_all_users(self,) -> list[tuple]:
        ans = self.cursor.execute(
            'SELECT * FROM User').fetchall()
        return ans

    async def get_user(self, user_id) -> tuple:
        ans = self.cursor.execute(
            'SELECT * FROM User WHERE id=?', [user_id]).fetchone()
        return ans

    async def update_user(self, user_info: dict):
        _str = 'UPDATE User SET'
        for key in user_info.keys():
            if not (key in ['id', 'name']):
                _str += f' {key}={user_info[key]},'
        _str = _str[:-1]
        _str += f" WHERE id = {user_info['id']}"
        self.cursor.execute(_str)
        self.db.commit()

    def get_name_tables(self,) -> list[str]:
        ans = self.cursor.execute(
            '''SELECT name FROM sqlite_master WHERE type='table';''').fetchall()
        return [i[0] for i in ans]


class DbHouse:

    def __init__(self, connect: sl.Connection, cursor: sl.Cursor):
        self.db = connect
        self.cursor = cursor

    async def create_new_table(self, name_table: str, args_list: list, ):
        _str = f'CREATE TABLE IF NOT EXISTS {name_table} ( date TEXT, id int,'
        for i in args_list:
            _str += f'"{i}" TEXT,'
            _str += f'"{i}_checkbox_handle" BOOLEAN,'
        _str = _str[:-1]
        _str += ')'
        self.cursor.execute(_str)
        self.db.commit()

    async def get_report_with_current_date(self, user_id: int, name_table: str) -> Union[dict[str, str], bool]:
        
        date = str(datetime.now().date())
        ans = self.cursor.execute(
            f"SELECT * FROM {name_table} WHERE id={user_id} AND date='{date}'").fetchone()
        cols = await self.get_name_cols_for_table(name_table)
        if ans:
            ans = list(ans)[2:]
        else:
            ans = []
            _str = f"INSERT INTO {name_table} VALUES('{date}', {user_id},"
            for i in cols:
                ans.append('')
                ans.append(False)
                _str += "'',"
                _str += "'',"
            _str = _str[:-1]
            _str += ')'
            self.cursor.execute(_str)
            self.db.commit()
        ans_dict = {}
        for i in range(len(cols)):
            ans_dict[cols[i]] = {'commentary': ans[i*2], 'checkbox': True if ans[i*2+1] else False}
        return ans_dict

    async def get_name_cols_for_table(self, name_table: str) -> list[str]:
        cols = self.cursor.execute(
            f'''PRAGMA table_info({name_table}) ''').fetchall()
        cols_res = []
        for i in cols:
            col_name = i[1]
            if not col_name in ['date', 'id'] and len(col_name.split('_checkbox_handle')) ==1:
                cols_res.append(col_name)
        return cols_res

    async def update_report(self, user_id: int, name_table: str, tasks: dict) -> None:
        date = str(datetime.now().date())
        ans = self.cursor.execute(
            f"SELECT * FROM {name_table} WHERE id={user_id} AND date='{date}'").fetchone()
        _str = f'UPDATE {name_table} SET'
        for key in tasks.keys():
            if 'commentary' in tasks[key].keys():
                _str += f" {key}='{tasks[key]['commentary']}',"
            if 'checkbox' in tasks[key].keys():
                _str += f"{key}__checkbox_handle={tasks[key]['checkbox']},"
        _str = _str[:-1]
        _str += f" WHERE id = {user_id} AND date='{date}'"
        self.cursor.execute(_str)
        self.db.commit()


class FullBd:

    def __init__(self,) -> None:
        self.connect = sl.connect(db_path)
        self.cursor = sl.Cursor(self.connect)
        self.db_users = UsersDatabaseConnector(self.connect, self.cursor)
        self.db_house = DbHouse(self.connect, self.cursor)
        self.db_users.create_table()


db = FullBd()
db_users = db.db_users
db_house = db.db_house
