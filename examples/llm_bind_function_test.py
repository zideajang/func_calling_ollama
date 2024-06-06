from rich.console import Console
console = Console()

from function_calling_ollama.llm.ollama.api import LocalModel,LocalModelConfig
from rich.console import Console
from function_calling_ollama.llm.ollama.api import LocalModel,LocalModelConfig
from function_calling_ollama.message.base import Message

from function_calling_ollama.prompt.prompt_template import FunctionCallingPromptTemplate
from function_calling_ollama.function_set.base import add,mul,sub,get_weather,get_directions
from function_calling_ollama.prompt.prompt_template import DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE


# TODO

llama3_config =  LocalModelConfig(
    endpoint="http://localhost:11434/",
    modelname="llama3",
    system=Message(role="system",content="you are very help assistant"),
    context_window=2048
)

local_model = LocalModel(llama3_config)
local_model.bind_tools([get_weather,get_directions])

response = local_model.query("What's the weather in Shenyang")
console.print(response)
console.print(type(response))
