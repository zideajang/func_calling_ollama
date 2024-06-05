from rich.console import Console
from function_calling_ollama.llm.ollama.api import LocalModel,LocalModelConfig
from function_calling_ollama.message.base import Message
from rich.console import Console
from function_calling_ollama.prompt.prompt_template import FunctionCallingPromptTemplate

function_template_prompt = FunctionCallingPromptTemplate()
prompt = function_template_prompt.format("What's the weather in shenyang")

console = Console()
console.print(prompt)

# TODO

llama3_config =  LocalModelConfig(
    endpoint="http://localhost:11434/",
    modelname="llama3",
    system=Message(role="system",content="you are very help assistant"),
    context_window=2048
)

local_model = LocalModel(llama3_config)
# local_model.bind
local_model.query(prompt)
