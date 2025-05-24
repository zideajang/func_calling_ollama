import types
from typing import List, Any, Optional, Dict
import json # 导入json模块以便序列化工具Schema

from function_calling_ollama.prompt.base import BasePromptTemplate
from function_calling_ollama.utils import function_to_json # 假设这个函数能返回类似OpenAI的函数定义格式
from function_calling_ollama.function_set.base import get_weather, get_directions # 示例工具函数

# DeepSeek 风格的工具调用提示模板
# DeepSeek模型通常使用 <tool_code>...</tool_code> 和 <tool_code_output>...</tool_code_output>
# 以及在 <tool_code> 内部包含结构化的JSON来表示工具调用
# DeepSeek 2.0 (DeepSeek-V2) 的 Function Calling 格式更接近 OpenAI，但仍然倾向于XML包裹
DEEPSEEK_FUNCTION_CALL_PROMPT_TEMPLATE = """
You are a helpful assistant with access to the following tools:
{tools_definition}

You must follow these instructions:
Always select one or more of the above tools based on the user query.
If a tool is found, you must respond with a <tool_code> block containing a JSON object for the tool call.
If multiple tools are required, respond with a list of <tool_code> blocks.
If no tool matches the user request, you should respond with a natural language answer.

Here is the user's request:
{prompt}
"""

# 旧的默认模板，可能适用于更通用的模型或早期的自定义模型
DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE = """
You have access to the following tools:
{tools_definition}
You must follow these instructions:
Always select one or more of the above tools based on the user query
If a tool is found, you must respond in the JSON format matching the following schema:
{{
    "tool_calls": [
        {{
            "name": "<name of the selected tool>",
            "arguments": <parameters for the selected tool, matching the tool's JSON schema>
        }}
    ]
}}
If there are multiple tools required, make sure a list of tool_calls are returned in a JSON array.
If there is no tool that match the user request, you will respond with empty json.
User Query: {prompt}
"""

class PromptTemplate(BasePromptTemplate):
    pass

class FunctionCallingPromptTemplate(BasePromptTemplate):

    def __init__(self, template: str, tool_format: str = "default"):
        super().__init__(template)
        self.tool_format = tool_format # "default" or "deepseek"

    @classmethod
    def from_template(cls, template: str, tool_format: str = "default"):
        
        return cls(template, tool_format=tool_format)

    def format(self, tools: Any, prompt: str) -> str:
        """
        根据指定的工具格式（default 或 deepseek）格式化工具定义。
        """
        print('format...')
        function_schema_list = []

        # 确保 tools 传入的是函数列表或预先格式化的字典列表
        if isinstance(tools, list) and tools:
            if isinstance(tools[0], types.FunctionType):
                for tool_func in tools:
                    function_schema_list.append(function_to_json(tool_func))
            elif isinstance(tools[0], dict) and "function" in tools[0]: # 假设传入的是OpenAI风格的tool dict
                function_schema_list = tools
            elif isinstance(tools[0], dict) and "name" in tools[0]: # 假设传入的是DeepSeek风格的tool dict (可能不太常见)
                function_schema_list = tools


        if self.tool_format == "deepseek":
            # DeepSeek 的工具定义通常会包裹在 <tool_code> 标签中，并且内部结构化
            # 这里需要将 function_schema_list 转换为 DeepSeek 模型能理解的格式
            # DeepSeek-V2 的工具定义格式通常是 JSON 数组，然后包裹在特殊的 XML 标签中
            # 例如: <available_tools> [ { "name": "...", "description": "...", "parameters": {} } ] </available_tools>
            
            # 简化示例，将所有工具的 JSON 定义串联起来，并用 <available_tools> 包裹
            print("deepseek reasoner")
            tools_json_str = json.dumps(function_schema_list, indent=2, ensure_ascii=False)

            formatted_tools_definition = f"<available_tools>\n{tools_json_str}\n</available_tools>"
            
            # 使用新的占位符 {tools_definition} 和 {prompt}

            return self.template.format(tools_definition=formatted_tools_definition, prompt=prompt)

        else: # default format
            # 对于默认格式，将函数 schema 列表直接转换为可读字符串，通常是JSON串联
            # 例如: [{"name": "get_weather", ...}, {"name": "get_directions", ...}]
            formatted_tools_definition = json.dumps(function_schema_list, indent=2, ensure_ascii=False)
            
            # 使用新的占位符 {tools_definition} 和 {prompt}
            return self.template.format(tools_definition=formatted_tools_definition, prompt=prompt)
