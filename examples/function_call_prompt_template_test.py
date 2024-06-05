from rich.console import Console
from function_calling_ollama.prompt.prompt_template import FunctionCallingPromptTemplate

console = Console()

function_template_prompt = FunctionCallingPromptTemplate()
prompt = function_template_prompt.format("What's the weather in shenyang")

console.print(prompt)