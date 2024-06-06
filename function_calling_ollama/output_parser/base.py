from __future__ import annotations
import json
from json import JSONDecodeError
import jsonpatch

from rich.console import Console

console = Console()

class OutPutJSONParser:
    @staticmethod
    def parser(str):
        try:
            res = json.loads(str)
            console.print(res)
        except:
            raise TypeError("can't convert data to json format")
            # reg 


if __name__ == "__main__":

    response_str = """
Here's my response:
{
    "tools": {
        "tool": "get_weather",
        "tool_input": {
        "city_name": "Shenyang"
        }
    }
}
"""

    response_in_json_format ="""
{
    "tools": {
        "tool": "get_weather",
        "tool_input": {
        "city_name": "Shenyang"
        }
    }
}

"""

OutPutJSONParser.parser(response_str)