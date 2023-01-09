from Utility.database_connector import db_users
import asyncio

def get_house_list():
    houses = db_users.get_name_tables()
    houses.remove('User')
    return houses

roles = db_users.get_columns_names()