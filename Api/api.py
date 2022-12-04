from fastapi import FastAPI, Form, Body
from pydantic import BaseModel
from typing import Union
import uvicorn
import traceback
import asyncio
from typing import Coroutine
from loguru import logger as log
from config import host_url, port
from Utility.database_connector import db_users


app = FastAPI()


def start_server():
    uvicorn.run(app, host=host_url, port=port)


class BaseItem(BaseModel):
    tg_id: int = None
    uid: str = None


class AdminList(BaseModel):
    list_admins: list


class AddUser(BaseModel):
    user_info: dict


class GetUser(BaseModel):
    user_id: int


async def bug_catcher(coro, name_debug, dict_required=False, data_required=True,):
    try:
        data = await coro
        if data_required:
            if dict_required:
                if type(data) == list:
                    for elem in range(len(data)):
                        data[elem] = data[elem].__dict__
                else:
                    data = data.__dict__
            return {'result': 'OK', 'data': data}
        else:
            return {'result': 'OK', 'data': 'OK'}
    except:
        log.debug(f'Ошибка /{name_debug}/\n{traceback.format_exc()}')
        return {'result': False}


@app.get('/get_admins')
async def get_admins():
    return await bug_catcher(db_users.get_admins(), 'get_admins')


@app.post('/add_admins/')
async def add_admins(item: AdminList):
    return await bug_catcher(db_users.add_admins(list_id=item.list_admins), 'add_admins', data_required=False)


@app.post('/add_user/')
async def add_user(item: AddUser):
    return await bug_catcher(db_users.add_user(user_info=item.user_info), 'add_user', data_required=False)


@app.get('/get_columns_names/')
async def get_columns_names():
    return await bug_catcher(db_users.get_columns_names(), 'get_columns_names')


@app.get('/get_all_users/')
async def get_all_users():
    return await bug_catcher(db_users.get_all_users(), 'get_all_users')


@app.get('/get_user/')
async def get_user(item: GetUser):
    return await bug_catcher(db_users.get_user(item.user_id), 'get_user')


@app.post('/delete_user/')
async def delete_user(item: GetUser):
    return await bug_catcher(db_users.delete_user(item.user_id), 'delete_user', data_required=False)


@app.post('/update_user/')
async def update_user(item: AddUser):
    return await bug_catcher(db_users.update_user(item.user_info), 'update_user', data_required=False)
