import sqlite3 as sl
from .classes import ConfigClass
import os


class UsersDatabaseConnector:
    """connector to database w/ users"""

    def __init__(self, connect: sl.connect, cursor: sl.Cursor):
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
                                engineer BOOLEAN,
                                )''')
        self.db.commit()


class FullBd:

    def __init__(self, cf: ConfigClass) -> None:
        self.connect = sl.connect(cf.db_path)
        self.cursor = sl.Cursor(self.connect)
        self.db_users = UsersDatabaseConnector(self.connect, self.cursor)
