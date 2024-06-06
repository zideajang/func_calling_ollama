import types
from typing import List,Any,Optional

from function_calling_ollama.prompt.base import BasePromptTemplate
from function_calling_ollama.utils import function_to_json
from function_calling_ollama.function_set.base import get_weather,get_directions

# TODO 
DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE = """
You have access to the following tools:
{0}
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
User Qeury: {1}


"""
class PromptTemplate(BasePromptTemplate):
    pass

class FunctionCallingPromptTemplate(BasePromptTemplate):

    def format(self,tools:Any,prompt):
        # TODO 后期优化为替换 placeholder
        function_schema_list = []
        if isinstance(tools[0],str):
            pass
        if isinstance(tools[0], types.FunctionType):
            for tool in tools:
                function_schema_json = function_to_json(tool)
                function_schema_list.append(function_schema_json)
        return self.template.format(function_schema_list,prompt)
    

