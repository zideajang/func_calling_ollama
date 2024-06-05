from typing import List,Any,Dict
from rich.console import Console

from urllib.parse import urljoin

from pydantic import BaseModel,Field
from function_calling_ollama.message.base import Message

import requests

OLLAMA_CHAT_API_BASE_URL = "/api/chat"
OLLAMA_COMPLETION_API_BASE_URL = "/api/generate"

class LocalChatModelConfig(BaseModel):
    endpoint:str
    modelname:str
    system:Message
    context_window:int = 8192

console = Console()

class LocalOllamaModel:

    def __init__(self,config:LocalChatModelConfig) -> None:
        self._config:LocalChatModelConfig = config
        self.endpoint = self._config.endpoint
        if not self.endpoint.startswith(("http://", "https://")):
            raise ValueError(f"Provided OPENAI_API_BASE value ({self.endpoint}) must begin with http:// or https://")

    def query(self,prompt:str,format="txt"):
        request = {
            "model":self._config.modelname,
            "prompt":prompt,
            "stream":False,
            "options":{
                "num_ctx":self._config.context_window
            }
        }
        if(format=="json"):
            request = request.update({
                "format":"json"
            })
        try:
            uri = urljoin(self.endpoint.strip("/") + "/" ,OLLAMA_COMPLETION_API_BASE_URL.strip("/"))
            response = requests.post(uri, json=request)
            print(response)
            print(response.status_code)
            if response.status_code == 200:
                result_full = response.json()
                console.print(f"JSON API response:\n{result_full}")
                result = result_full["response"]
                print(result)

            else:
                Exception(
                    f"API call got non-200 response code (code={response.status_code}, msg={response.text}) for address: {uri}."
                    + f" Make sure that the ollama API server is running and reachable at {uri}."
                )
        except:
            print("some error")
            raise 
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
    llama3_config =  LocalChatModelConfig(
        endpoint="http://localhost:11434/",
        modelname="llama3",
        system=Message(role="system",content="you are very help assistant\nASSISTANT:"),
        context_window=2048
    )

    local_model = LocalOllamaModel(llama3_config)
    local_model.query("why the sky is blue")


        