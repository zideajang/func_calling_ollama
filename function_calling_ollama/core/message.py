from typing import Literal,Optional
from pydantic import BaseModel,Field

class Message(BaseModel):
    role:Literal['user', 'assistant', 'system','tool'] = Field(title="在对话中信息的来源")
    content:str
    name: Optional[str] = Field(None, title="工具的名称，当role为'tool'时使用")
