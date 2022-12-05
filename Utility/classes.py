from dataclasses import dataclass
from aiogram.types import Message


@dataclass
class UserInfo:
    name: str
    id: int
    admin: bool = False
    it: bool = False
    electrical: bool = False
    fireman: bool = False
    engineer: bool = False


@dataclass
class TempData:
    name_table:str=None
    tasks:str = None
    role:str = None
    page:int = 0