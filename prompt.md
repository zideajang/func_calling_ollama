```json
{
  "name": "get_directions",
  "description": "Get directions from Google Directions API.\n    start: start address as a string including zipcode (if any)\n    destination: end address as a 
string including zipcode (if any)",
  "parameters": {
    "type": "object",
    "properties": {
      "start": {
        "type": "str"
      },
      "destination": {
        "type": "str"
      }
    }
  },
  "returns": "Direction"
}
```
上面是描述函数 
```python
class Weather:
    pass

def get_weather(city_name:str)->Weather:
    """Get the current weather given a city"""
    #TODO implement this to actually call it later

```
的 function schema

写一个 prompt 让 ollama 根据用户 query 学会调用工具来解决用户的问题的 prompt

如下面例子，字符串 response 中除了有 json 格式数据还有其他字符串
response = """
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
利用 python 中 re 正则表达式方式将 json 数据提取出来进行解析 json_dump