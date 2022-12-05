import aiohttp
import asyncio
from dataclasses import dataclass
from typing import Union
from config import host_url, port
from Utility.classes import UserInfo


@dataclass
class Http:

    async def req(self, url, data=None, method='GET'):
        for i in range(5):
            try:
                async with aiohttp.request(method, f'http://{host_url}:{port}/{url}', json=data) as resp:
                    json = await resp.json()
                    if resp.status != 200 or json['result'] != 'OK':
                        raise
                    return json['data']
            except:
                pass
    # users

    async def get_admins(self,) -> list[UserInfo]:
        ans = await self.req('get_admins/')
        list_res = []
        for i in ans:
            list_res.append(UserInfo(*i))
        return list_res

    async def add_admins(self, list_admins: list) -> None:
        ans = await self.req('add_admins/', data={'list_admins': list_admins}, method='POST')

    async def add_user(self, user_info: dict) -> None:
        ans = await self.req('add_user/', data={'user_info': user_info}, method='POST')

    async def get_columns_names(self,) -> list[str]:
        ans = await self.req('get_columns_names/')
        return ans

    async def get_user(self, user_id: int) -> UserInfo:
        ans = await self.req('get_user/', data={'user_id': user_id})
        return UserInfo(*ans)

    async def get_name_tables(self) -> list[str]:
        ans = await self.req('get_name_tables/')
        return ans

    async def delete_user(self, user_id: int) -> None:
        ans = await self.req('delete_user/', data={'user_id': user_id}, method='POST')

    async def update_user(self, user_info: dict) -> None:
        ans = await self.req('update_user/', data={'user_info': user_info}, method='POST')

    async def get_all_users(self,) -> list[UserInfo]:
        ans = await self.req('get_all_users/')
        list_res = []
        for i in ans:
            list_res.append(UserInfo(*i))
        return list_res

    # houses
    async def create_new_table(self, name_table: str, args_list: list,) -> None:
        ans = await self.req('create_new_table/', data={'name_table': name_table, 'args_list': args_list}, method='POST')

    async def get_report_with_current_date(self,  user_id: int, name_table: str) -> Union[dict[str, str], bool]:
        ans = await self.req('get_report_with_current_date/', data={'user_id': user_id, 'name_table': name_table})
        return ans

    async def get_name_cols_for_table(self, name_table: str) -> list[str]:
        ans = await self.req('get_name_cols_for_table/', data={'name_table': name_table})
        return ans

    async def update_report(self, user_id: int, name_table: str, tasks: dict) -> None:
        ans = await self.req('update_report/', data={'user_id': user_id, 'name_table': name_table, 'tasks': tasks}, method='POST')


http = Http()
