from rich.console import Console

from function_calling_ollama.core import LocalModel,LocalModelConfig
from function_calling_ollama.core import Message

console = Console()

llama3_config_sync = LocalModelConfig(
    endpoint="http://localhost:11434/",
    modelname="llama3.1:latest",
    system=Message(role="system", content="You are a helpful assistant."),
    context_window=2048,
    supports_native_tools=True 
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
    if not sync_response_with_tools['message']['content'] and 'tool_calls' in sync_response_with_tools['message']:
        console.print("[yellow]Model wants to call a tool![/yellow]")
        tool_calls = sync_response_with_tools['message']['tool_calls']

        # Iterate through all tool calls the model suggests
        for tool_call in tool_calls:
            function_name = tool_call['function']['name']
            arguments = tool_call['function']['arguments']

            # Check if the function exists in our local environment
            if function_name == "get_current_weather": # You'd expand this for other tools
                console.print(f"[green]Calling local function: {function_name} with arguments: {arguments}[/green]")
                # Execute the function with the provided arguments
                # Note: This assumes arguments are simple kwargs.
                # For complex arguments, you might need more sophisticated parsing.
                function_result = get_current_weather(**arguments)
                console.print(f"[blue]Function result: {function_result}[/blue]")

                # Optionally, you can send this result back to the model
                # as a tool message to get a natural language response.
                messages_with_tools_sync.append(Message(
                    role="tool",
                    content=str(function_result), # Convert result to string
                    name=function_name
                ))
                # Get a final response from the model using the tool output
                final_response = sync_model.chat_sync(messages_with_tools_sync)
                console.print(f"Final Model Response (after tool call): {final_response['message']['content']}")
            else:
                console.print(f"[red]Error: Unknown tool function requested: {function_name}[/red]")
    else:
        # If the model provides a direct content response or no tool calls
        console.print(f"Sync Chat Response with Tools: {sync_response_with_tools['message']['content']}")
    # --- End of the added logic ---

except Exception as e:
    console.print(f"Error during synchronous chat with injected tools: {e}", style="red")
