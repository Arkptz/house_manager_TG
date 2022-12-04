from dataclasses import dataclass

@dataclass
class UserInfo:
    name:str
    id:int
    admin:bool=False
    it:bool=False
    electrical:bool=False
    fireman:bool=False
    engineer:bool=False
