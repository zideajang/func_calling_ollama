import json

from rich.console import Console
from function_calling_ollama.llm.ollama.api import LocalModel,LocalModelConfig
from function_calling_ollama.message.base import Message

from function_calling_ollama.prompt.prompt_template import FunctionCallingPromptTemplate
from function_calling_ollama.function_set.base import add,mul,sub,get_weather,call_tool
from function_calling_ollama.prompt.prompt_template import DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE
from langchain.output_parsers.json import SimpleJsonOutputParser
console = Console()

function_calling_template_prompt = FunctionCallingPromptTemplate.from_template(DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE)
prompt = function_calling_template_prompt.format(
    tools=[add,mul,sub,get_weather],
    prompt="What's the weather in shenyang")

# console.print(prompt)~

# TODO

llama3_config =  LocalModelConfig(
    endpoint="http://localhost:11434/",
    modelname="llama3:instruct",
    system=Message(role="system",content="you are very help assistant"),
    context_window=2048
)

local_model = LocalModel(llama3_config)
# local_model.bind
response = local_model.query(prompt.strip().replace('\\n','').strip())
console.print(response)
console.print(type(response))
json_parser = SimpleJsonOutputParser()
response = json_parser.parse(response)
console.print(response)
call_tool(response,func=None)
