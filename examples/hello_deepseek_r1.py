import re
import json
from rich.console import Console

from function_calling_ollama.core import LocalModel,LocalModelConfig
from function_calling_ollama.core import Message

console = Console()

llama3_config_sync = LocalModelConfig(
    endpoint="http://localhost:11434/",
    modelname="deepseek-r1:latest",
    system=Message(role="system", content="You are a helpful assistant."),
    context_window=2048,
    supports_native_tools=False 
)

sync_model = LocalModel(llama3_config_sync)

console.print("\n--- Synchronous Chat Example ---",justify="center")

try:
    messages_sync = [
        Message(role="user", content="Tell me a joke.")
    ]
    sync_response = sync_model.chat_sync(messages_sync)
    console.print(f"Sync Chat Response: {sync_response['message']['content']}")
except Exception as e:
    console.print(f"Error during synchronous chat: {e}", style="red")

console.print("\n--- Synchronous Chat with Injected Tools Example ---")
try:
    def get_current_weather(location: str):
        """Get the current weather in a given location."""
        if location == "London":
            return {"temperature": "15C", "conditions": "cloudy"}
        elif location == "Paris":
            return {"temperature": "20C", "conditions": "sunny"}
        return {"temperature": "N/A", "conditions": "unknown"}

    tools_example = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        }
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    sync_model.bind_tools(tools_example)
    
    messages_with_tools_sync = [
        Message(role="user", content="What's the weather like in London?")
    ]

    sync_response_with_tools = sync_model.chat_sync(messages_with_tools_sync)

    console.print(sync_response_with_tools)

    match = re.search(r'<tool_code>(.*?)</tool_code>', sync_response_with_tools['message']['content'], re.DOTALL)
    console.print(match)
    if match:
        tool_json_str = match.group(1).strip()  # <--- Added .strip() here
        console.print("--"*50)
        console.print(tool_json_str.replace('<tool_code>',''))
        tool_data = json.loads(tool_json_str.replace('<tool_code>',''))

        console.print(tool_data)

        # Extract function name and arguments
        function_name = tool_data['function']['name']
        
        # In a real tool call from a model, the arguments would be in a "tool_calls" part of the response.
        # For this example, we infer "London" from the context of the user's query.
        # The provided JSON describes the tool, not a specific call to it with arguments.
        # We will assume the model would generate something like:
        # {"tool_calls": [{"function": {"name": "get_current_weather", "arguments": {"location": "London"}}}]}
        # For this demonstration, we'll hardcode the arguments to simulate the call.
        
        if function_name == "get_current_weather":
            arguments = {"location": "London"} 
            
            # Call the corresponding function
            result = get_current_weather(**arguments)
            print(f"Function call result: {result}")
        else:
            print(f"Unknown function: {function_name}")
    else:
        print("No <tool_code> block found.")

    console.print(sync_response_with_tools)

    

except Exception as e:
    console.print(f"Error during synchronous chat with injected tools: {e}", style="red")
