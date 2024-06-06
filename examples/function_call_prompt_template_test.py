from rich.console import Console
from function_calling_ollama.prompt.prompt_template import FunctionCallingPromptTemplate
from function_calling_ollama.prompt.prompt_template import DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE
from function_calling_ollama.function_set.base import add,mul,sub,get_weather

console = Console()
# 

function_calling_template_prompt = FunctionCallingPromptTemplate.from_template(DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE)
console.print(function_calling_template_prompt)

prompt = function_calling_template_prompt.format(
    tools=[add,mul,sub],
    prompt="What's the weather in shenyang")

console.print(prompt)