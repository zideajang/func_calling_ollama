from pydantic import BaseModel
from dataclasses import dataclass

class BasePromptTemplate(BaseModel):
    template:str
    
    @classmethod
    def from_template(cls,template:str):
        return cls(template=template)

    def format(self,prompt:str)->str:
        pass

