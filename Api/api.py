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


async def bug_catcher(coro: function, name_debug, dict_required=True, data_required=True):
    try:
        data = coro()
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
    return await bug_catcher(db_users.get_admins, 'get_admins', dict_required=False)
