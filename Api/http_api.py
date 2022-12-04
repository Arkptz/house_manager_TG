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

    async def get_users_not_admin(self,) -> list[UserInfo]:
        ans = await self.req('get_users_not_admin/')
        list_res = []
        for i in ans:
            list_res.append(UserInfo(*i))
        return list_res

    async def remove_admin(self, user_id: int) -> None:
        ans = await self.req('remove_admin/', data={'user_id': user_id}, method='POST')

    async def get_columns_names(self,) -> list[str]:
        ans = await self.req('get_columns_names/')
        return ans

    async def get_all_users(self,) -> list[UserInfo]:
        ans = await self.req('get_all_users/')
        list_res = []
        for i in ans:
            list_res.append(UserInfo(*i))
        return list_res


http = Http()
