from Utility.database_connector import db_users
import asyncio


houses = db_users.get_name_tables()
houses.remove('User')
roles = db_users.get_columns_names()
