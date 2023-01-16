from fastapi import FastAPI, Form, Body, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Union
import uvicorn
import traceback
import asyncio
from Utility.classes import UserInfo
from typing import Coroutine
from loguru import logger as log
from config import host_url, port
from Utility.database_connector import db_users, db_house

app = FastAPI()
# app.mount("/new_checklist/static", StaticFiles(directory=r"A:\Документы\GitHub\house_manager_TG\Api\templates\new_checklist\static"), name="static")
# templates = Jinja2Templates(
#     directory=r"A:\Документы\GitHub\house_manager_TG\Api\templates")


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


class NewTable(BaseModel):
    name_table: str
    args_list: list


class AddTranslate(BaseModel):
    original: str
    translate: str


class GetReport(BaseModel):
    user_id: int
    name_table: str


class GetCols(BaseModel):
    name_table: str


class AddHouse(BaseModel):
    name: str
    access: str
    tasks: list
    # {'name': .., 'access': 'admin/it/electrical/fireman/engineer', tasks: ['task1', 'task2']}
    user_id: str


class AddUserWA(BaseModel):
    name: str
    id: str
    access: str
    user_id: str


class UpdateReport(BaseModel):
    user_id: int
    name_table: str
    tasks: dict


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

# users


# @app.get('/new-checklist', response_class=HTMLResponse)
# async def new_checklist(request: Request):
#     return templates.TemplateResponse("new_checklist/index.html", {"request": request})




@app.get('/get_admins')
async def get_admins():
    return await bug_catcher(db_users.get_admins(), 'get_admins')


@app.post('/add_admins/')
async def add_admins(item: AdminList):
    return await bug_catcher(db_users.add_admins(list_users=item.list_admins), 'add_admins', data_required=False)


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


@app.get('/get_name_tables/')
async def get_name_tables():
    return await bug_catcher(db_users.get_name_tables(), 'get_name_tables')


# houses
@app.post('/create_new_table/')
async def create_new_table(item: NewTable):
    return await bug_catcher(db_house.create_new_table(name_table=item.name_table, args_list=item.args_list),
                             'create_new_table', data_required=False)


@app.get('/get_report_with_current_date/')
async def get_report_with_current_date(item: GetReport):
    return await bug_catcher(db_house.get_report_with_current_date(item.user_id, item.name_table),
                             'get_report_with_current_date')


@app.get('/get_name_cols_for_table/')
async def get_name_cols_for_table(item: GetCols):
    return await bug_catcher(db_house.get_name_cols_for_table(item.name_table),
                             'get_name_cols_for_table')


@app.post('/update_report/')
async def update_report(item: UpdateReport):
    return await bug_catcher(db_house.update_report(item.user_id, item.name_table, item.tasks),
                             'update_report', data_required=False)


# webapps

@app.post('/add_house/')
async def add_house(req: Request):
    data = await req.form()
    user_id = data.get('id')
    if user_id != '':
        args_list = []
        task = 1
        arg = data.get(f'task_{task}')
        while arg:
            task +=1
            args_list.append(arg)
            arg = data.get(f'task_{task}')
            
        await bug_catcher(db_house.create_new_table(name_table=f'{data.get("name")}_{data.get("access")}', args_list=args_list),
                                 'create_new_table', data_required=False)
    return HTMLResponse( content=
		'<script type="text/javascript" src="https://telegram.org/js/telegram-web-app.js"></script>' 
		'<script>Telegram.WebApp.ready();Telegram.WebApp.close();</script>', status_code=200)


@app.post('/add_userWA/')
async def add_userWA(item: AddUserWA):
    if item.user_id:
        user_info = UserInfo(item.name, item.id, )
        setattr(user_info, item.access, True)
        return await bug_catcher(db_users.add_user(user_info=user_info.__dict__), 'add_user', data_required=False)
