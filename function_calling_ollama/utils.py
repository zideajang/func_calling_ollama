import json
import inspect

from typing import get_type_hints

import tiktoken

from typing import get_type_hints
from rich.console import Console

from function_calling_ollama.function_set.base import add


console = Console()

DEBUG = True

def count_tokens(s: str, model: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(s))


def printd(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def outputParser(response:str):
    try:
        res = response.strip().replace("\n","").replace("\\","")
        console.print_json(res)
        return res
    except Exception:
        console.print(f"Unable to decode JSON {response}")


def get_type_name(t):
    name = str(t)
    if "list" in name or "dict" in name:
        return name
    else:
        return t.__name__


def function_to_json(func):
    signature = inspect.signature(func)
    # console.log(signature)
    type_hints = get_type_hints(func)
    # console.print(type_hints)
    # console.print(type_hints.get('a').__name__)

    # 获取到函数的描述
    console.print(f"name: {func.__name__}")
    console.print(f"description:{func.__doc__}" )

    function_info = {
        "name": func.__name__,
        "description": func.__doc__,
        "parameters": {"type": "object", "properties": {}},
        "returns": type_hints.get("return", "void").__name__,
    }

    # console.print(signature.parameters.items())

    for name, _ in signature.parameters.items():
        param_type = get_type_name(type_hints.get(name, type(None)))
        function_info["parameters"]["properties"][name] = {"type": param_type}

    return json.dumps(function_info, indent=2)


def func_call(tool_func:list[dict])->list[str]:
    pass

if __name__ == "__main__":
    add_function_schema = function_to_json(add)
    console.print_json(add_function_schema)