from function_calling_ollama.llm.ollama.api import LocalModel,LocalModelConfig
from function_calling_ollama.message.base import Message

llama3_config =  LocalModelConfig(
    endpoint="http://localhost:11434/",
    modelname="llama3",
    system=Message(role="system",content="you are very help assistant\nASSISTANT:"),
    context_window=2048
)

local_model = LocalModel(llama3_config,format="json")
local_model.query("why the sky is blue")
