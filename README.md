# func_calling_ollama
models in ollama support the function calling feature

## 安装
```python
pip install -e .
```

## 快速入门
```python
What's the weather in shenyang
```

```python
{
  "tools": {
    "tool": "get_weather",
    "tool_input": {
      "city_name": "Shenyang"
    }
  }
}
```

```shell
{
  "tools": {
    "tool": "get_weather",
    "tool_input": {
      "city_name": "shenyang"
    }
  }
}
<class 'str'>
{'tools': {'tool': 'get_weather', 'tool_input': {'city_name': 'shenyang'}}}
Fetching weather for shenyang...
Weather in shenyang: Sunny with mild temperatures.
```

```
Here's my response:

{
  "tools": {
    "tool": "get_weather",
    "tool_input": {
      "city_name": "Shenyang"
    }
  }
}
```