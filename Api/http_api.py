import aiohttp
import asyncio
from dataclasses import dataclass
from typing import Union
from config import host_url, port
from Utility.classes import AdminInfo


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

    async def get_admins(self,) ->list[AdminInfo]:
        ans = await self.req('/get_admins/')
        list_res = []
        for i in ans:
            list_res.append(AdminInfo(*i))
        return list_res

http = Http()