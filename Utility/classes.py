from dataclasses import dataclass

@dataclass
class AdminInfo:
    name:str
    id:int
    admin:bool
    it:bool
    electrical:bool
    fireman:bool
    engineer:bool