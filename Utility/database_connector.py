import sqlite3 as sl
from config import db_path
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
                                id TEXT,
                                admin BOOLEAN,
                                it BOOLEAN,
                                electrical BOOLEAN,
                                fireman BOOLEAN,
                                engineer BOOLEAN
                                )''')
        self.db.commit()

    async def get_admins(self,) -> list[tuple]:
        ans = self.cursor.execute('SELECT * FROM User WHERE admin').fetchall()
        return ans

    async def add_admins(self, list_id: list) -> None:
        for user_id in list_id:
            data = self.cursor.execute(
                'SELECT * FROM User WHERE id=?', [user_id]).fetchall()
            if len(data) == 0:
                self.cursor.execute(
                    'INSERT INTO User (id, admin) VALUES(?,?)', [user_id, True])
        self.db.commit()

    async def add_user(self, user_info: dict):
        self.cursor.execute('INSERT INTO USER VALUES(???????)', [
                            user_info['name'], user_info['id'], user_info['admin'], '', '', '', ''])


class FullBd:

    def __init__(self,) -> None:
        self.connect = sl.connect(db_path)
        self.cursor = sl.Cursor(self.connect)
        self.db_users = UsersDatabaseConnector(self.connect, self.cursor)
        self.db_users.create_table()


db = FullBd()
db_users = db.db_users
