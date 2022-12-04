import aiohttp
import asyncio
from dataclasses import dataclass
from typing import Union
from ..classes import ConfigClass


@dataclass
class http:
    cf: ConfigClass

    async def req(self, url, data=None, method='GET'):
        for i in range(5):
            try:
                async with aiohttp.request(method, f'http://{self.cf.host_url}:{self.cf.port}/{url}', json=data) as resp:
                    json = await resp.json()
                    if resp.status != 200 or json['result'] != 'OK':
                        raise
                    return json['data']
            except:
                pass

    