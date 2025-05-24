import asyncio
from rich.console import Console

from function_calling_ollama.core import LocalModel,LocalModelConfig
from function_calling_ollama.core import Message

console = Console()

async def main():
    llama3_config_async = LocalModelConfig(
        endpoint="http://localhost:11434/",
        modelname="llama3",
        system=Message(role="system", content="You are a poetic assistant."),
        context_window=2048,
        supports_native_tools=False # Assume llama3 does not natively support tools
    )
    
    async_model = LocalModel(llama3_config_async)

    print("\n--- Asynchronous Chat Example ---")
    try:
        messages_async = [
            Message(role="user", content="Write a short poem about the sea.")
        ]
        async_response = await async_model.chat(messages_async)
        print(f"Async Chat Response: {async_response['message']['content']}")
    except Exception as e:
        console.print(f"Error during asynchronous chat: {e}", style="red")

    print("\n--- Asynchronous Chat with Injected Tools Example ---")
    try:
        # Re-using the tools_example from sync example
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
        async_model.bind_tools(tools_example)
        messages_with_tools_async = [
            Message(role="user", content="What's the weather in Paris?")
        ]
        async_response_with_tools = await async_model.chat(messages_with_tools_async)
        print(f"Async Chat with Injected Tools Response: {async_response_with_tools['message']['content']}")
    except Exception as e:
        console.print(f"Error during asynchronous chat with injected tools: {e}", style="red")

    # Example with native tool support (if a model like 'llama3-chat-functions' were available)
    print("\n--- Asynchronous Chat with Native Tools (Conceptual) ---")
    try:
        native_tool_config = LocalModelConfig(
            endpoint="http://localhost:11434/",
            modelname="llama3-with-tools", # A hypothetical model that supports native tools
            system=Message(role="system", content="You are a helpful assistant with access to tools."),
            context_window=4096,
            supports_native_tools=True # This model *does* natively support tools
        )
        native_tool_model = LocalModel(native_tool_config)
        native_tool_model.bind_tools(tools_example) # Bind the same tools

        messages_native_tools = [
            Message(role="user", content="What's the weather like in London?")
        ]
        native_tool_response = await native_tool_model.chat(messages_native_tools)
        print(f"Native Tools Chat Response: {native_tool_response['message']['content']}")
        # In a real scenario, you'd expect 'tool_calls' in the response for native tool support
    except Exception as e:
        console.print(f"Error during native tools chat: {e}", style="red")
    
    await async_model._async_client.aclose() # Explicitly close async client
    await native_tool_model._async_client.aclose() # Explicitly close async client

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())

    # Closing sync client explicitly for main script