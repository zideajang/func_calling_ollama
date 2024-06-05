from typing import Literal
from pydantic import BaseModel,Field

class Message(BaseModel):
    role:Literal['user', 'assistant', 'system']
    content:str

