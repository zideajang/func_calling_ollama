from typing import List,Any,Dict
from rich.console import Console

from urllib.parse import urljoin

from pydantic import BaseModel,Field
from function_calling_ollama.message.base import Message
from function_calling_ollama.prompt.prompt_template import FunctionCallingPromptTemplate
from function_calling_ollama.prompt.prompt_template import DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE

import requests

OLLAMA_CHAT_API_BASE_URL = "/api/chat"
OLLAMA_COMPLETION_API_BASE_URL = "/api/generate"

class LocalModelConfig(BaseModel):
    endpoint:str
    modelname:str
    system:Message
    context_window:int = 8192

console = Console()

class LocalModel:

    def __init__(self,config:LocalModelConfig) -> None:
        self._config:LocalModelConfig = config
        self.endpoint = self._config.endpoint
        
        self.tools = []

        if not self.endpoint.startswith(("http://", "https://")):
            raise ValueError(f"Provided OPENAI_API_BASE value ({self.endpoint}) must begin with http:// or https://")

    def query(self,prompt:str,format="txt"):
        if self.tools:
            prompt_template = FunctionCallingPromptTemplate.from_template(DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE)
            query_prompt = prompt_template.format(tools=self.tools,prompt=prompt)
        else:
            query_prompt = prompt
        payload = {
            "model":self._config.modelname,
            "prompt":query_prompt.strip(),
            "stream":False,
            "options":{
                "num_ctx":self._config.context_window
            },
            "raw":False,
        }
        if(format=="json"):
            payload = payload.update({
                "format":"json"
            })
        console.print(payload)
        try:
            uri = urljoin(self.endpoint.strip("/") + "/" ,OLLAMA_COMPLETION_API_BASE_URL.strip("/"))
            response = requests.post(uri, json=payload)
            print(response)
            print(response.status_code)
            if response.status_code == 200:
                result_full = response.json()
                # console.print(f"JSON API response:\n{result_full}")
                console.print(type(result_full['response']))
                result = result_full["response"]
                return result

            else:
                Exception(
                    f"API call got non-200 response code (code={response.status_code}, msg={response.text}) for address: {uri}."
                    + f" Make sure that the ollama API server is running and reachable at {uri}."
                )
        except:
            print("some error")
            raise 
    
    def bind_tools(self,tools:List[Any]):
        self.tools.extend(tools)
    
    def chat(self,messages:List[Message]):
        request = {
            "model":self._config.model_name,
            "messages":messages.append(self._config.system),
            "options": {
                "seed": 101,
                "temperature": 0
            },
            "raw":True
        }
        # try:
        #     uri = urljoin(self.endpoint.strip("/") + "/" ,OLLAMA_CHAT_API_BASE_URL.strip("/"))
        #     response = requests.post(uri, json=request)

    def batch_chat(self,batch:List[List[Message]]):
        pass



if __name__ == "__main__":
    llama3_config =  LocalModel(
        endpoint="http://localhost:11434/",
        modelname="llama3",
        system=Message(role="system",content="you are very help assistant\nASSISTANT:"),
        context_window=2048
    )

    local_model = LocalModel(llama3_config)
    local_model.query("why the sky is blue")


        