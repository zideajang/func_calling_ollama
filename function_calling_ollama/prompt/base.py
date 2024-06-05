from typing import Protocol

class BasePromptTemplate(Protocol):
    def format(self,prompt:str)->str:
        pass

