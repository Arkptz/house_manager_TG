from fastapi import FastAPI, Form, Body
from pydantic import BaseModel
from typing import Union
import uvicorn
import traceback
import asyncio
from typing import Coroutine
from loguru import logger as log
from ..classes import ConfigClass
from ..database_connector import FullBd


app = FastAPI()


def start_server(cf: ConfigClass):
    global db
    db = FullBd(cf)
    uvicorn.run(app, host=cf.host_url, port=cf.port)


class BaseItem(BaseModel):
    tg_id: int = None
    uid: str = None


async def bug_catcher(coro: Coroutine, name_debug, dict_required=True, data_required=True):
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

# Users part
