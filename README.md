# func_calling_ollama
models in ollama support the function calling feature

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