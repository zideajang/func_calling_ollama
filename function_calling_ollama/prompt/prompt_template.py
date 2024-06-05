from function_calling_ollama.prompt.base import BasePromptTemplate
from function_calling_ollama.utils import function_to_json
from function_calling_ollama.function_set.base import get_weather,get_directions

# TODO 
class FunctionCallingPromptTemplate(BasePromptTemplate):

    def __init__(self) -> None:
        self.template = f"""
You have access to the following tools:
{function_to_json(get_weather)}
{function_to_json(get_directions)}
You must follow these instructions:
Always select one or more of the above tools based on the user query
If a tool is found, you must respond in the JSON format matching the following schema:
{{
   "tools": {{
        "tool": "<name of the selected tool>",
        "tool_input": <parameters for the selected tool, matching the tool's JSON schema
   }}
}}
If there are multiple tools required, make sure a list of tools are returned in a JSON array.
If there is no tool that match the user request, you will respond with empty json.
User Qeury: 
    """
    def format(self,prompt):
        # TODO 后期优化为替换 placeholder
        return self.template + prompt