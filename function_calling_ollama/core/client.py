from typing import List, Any, Dict
from rich.console import Console
from urllib.parse import urljoin
from pydantic import BaseModel, Field
import httpx

from .message import Message
from function_calling_ollama.prompt.prompt_template import FunctionCallingPromptTemplate
from function_calling_ollama.prompt.prompt_template import DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE,DEEPSEEK_FUNCTION_CALL_PROMPT_TEMPLATE

OLLAMA_CHAT_API_BASE_URL = "/api/chat"
OLLAMA_COMPLETION_API_BASE_URL = "/api/generate"

class LocalModelConfig(BaseModel):
    endpoint: str
    modelname: str
    system: Message
    context_window: int = Field(default=8192)
    # 这个字段表示模型是否原生支持工具的调用
    supports_native_tools: bool = Field(default=False)

console = Console()
IS_DEBUG = True

class LocalModel:
    def __init__(self, config: LocalModelConfig) -> None:
        self._config: LocalModelConfig = config
        self.endpoint = self._config.endpoint
        self._client = httpx.Client()
        self._async_client = httpx.AsyncClient()
        self.tools = []

        if not self.endpoint.startswith(("http://", "https://")):
            raise ValueError(f"Provided endpoint value ({self.endpoint}) must begin with http:// or https://")

    def _get_chat_url(self) -> str:
        return urljoin(self.endpoint.strip("/") + "/", OLLAMA_CHAT_API_BASE_URL.strip("/"))

    def _get_completion_url(self) -> str:
        return urljoin(self.endpoint.strip("/") + "/", OLLAMA_COMPLETION_API_BASE_URL.strip("/"))

    def query(self, prompt: str, format="txt"):
        # This method uses the old /api/generate endpoint, which is not ideal for chat or tools
        # Consider refactoring to use chat_sync or chat directly for consistency
        if self.tools and not self._config.supports_native_tools:
            prompt_template = FunctionCallingPromptTemplate.from_template(DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE)
            query_prompt = prompt_template.format(tools=self.tools, prompt=prompt)
        else:
            query_prompt = prompt

        payload = {
            "model": self._config.modelname,
            "prompt": query_prompt.strip(),
            "stream": False,
            "options": {
                "num_ctx": self._config.context_window
            },
            "raw": False,
        }
        if format == "json":
            payload.update({"format": "json"})

        console.print(payload)
        try:
            uri = self._get_completion_url()
            response = self._client.post(uri, json=payload)
            print(response)
            print(response.status_code)
            if response.status_code == 200:
                result_full = response.json()
                console.print(type(result_full['response']))
                result = result_full["response"]
                return result
            else:
                raise Exception(
                    f"API call got non-200 response code (code={response.status_code}, msg={response.text}) for address: {uri}."
                    + f" Make sure that the ollama API server is running and reachable at {uri}."
                )
        except httpx.RequestError as e:
            console.print(f"An error occurred while requesting {e.request.url!r}.")
            raise
        except Exception as e:
            console.print(f"An unexpected error occurred: {e}")
            raise

    def bind_tools(self, tools: List[Dict[str, Any]]):
        """
        Binds tools to the model.
        Tools should be in a format that Ollama expects for function calling (if native support).
        If native tool support is not enabled, tools will be injected into the system prompt.
        """
        self.tools.extend(tools)

    def _prepare_chat_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        # Include the system message from config
        # 确保 system 消息是字典形式
        all_messages = [self._config.system.model_dump()] + [m.model_dump() for m in messages]

        # If native tool support is not enabled, inject tools into the system prompt
        if not self._config.supports_native_tools and self.tools:
            # 确定使用哪个模板和工具格式
            template_str = DEEPSEEK_FUNCTION_CALL_PROMPT_TEMPLATE if self._config.modelname.startswith("deepseek") else DEFAULT_FUNCTION_CALL_PROMPT_TEMPLATE
            
            # 传递 tool_format 参数给 FunctionCallingPromptTemplate
            tool_format_type = "deepseek" if self._config.modelname.startswith("deepseek") else "default"
            
            prompt_template = FunctionCallingPromptTemplate.from_template(template_str, tool_format=tool_format_type)

            tool_injection_prompt = prompt_template.format(tools=self.tools, prompt="")
            
            # 在这里，prompt="" 意味着工具定义部分不包含用户查询，只包含工具信息
            # Find the existing system message and prepend the tool injection
            system_message_found = False
            for msg in all_messages:
                if msg.get("role") == "system":
                    # 将工具注入内容添加到现有 system 消息的开头
                    msg["content"] = tool_injection_prompt + "\n" + msg["content"]
                    system_message_found = True
                    break
            
            # If no system message exists, add one at the beginning
            if not system_message_found:
                all_messages.insert(0, {"role": "system", "content": tool_injection_prompt})

        return all_messages

    async def chat(self, messages: List[Message]) -> Dict[str, Any]:
        """
        Performs an asynchronous chat completion.
        """
        payload = {
            "model": self._config.modelname,
            "messages": self._prepare_chat_messages(messages),
            "options": {
                "seed": 101,
                "temperature": 0.0 # Using 0.0 for deterministic responses
            },
            "stream": False,
        }
        
        # If native tool support is enabled, include the tools in the payload
        if self._config.supports_native_tools and self.tools:
            payload["tools"] = self.tools

        console.print(f"Chat payload: {payload}")

        try:
            uri = self._get_chat_url()
            response = await self._async_client.post(uri, json=payload, timeout=60.0) # Add a timeout
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except httpx.RequestError as e:
            console.print(f"An error occurred while requesting {e.request.url!r}.")
            raise
        except httpx.HTTPStatusError as e:
            console.print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            console.print(f"An unexpected error occurred during async chat: {e}")
            raise

    def chat_sync(self, messages: List[Message]) -> Dict[str, Any]:
        """
        Performs a synchronous chat completion.
        """
        payload = {
            "model": self._config.modelname,
            "messages": self._prepare_chat_messages(messages),
            "options": {
                "seed": 101,
                "temperature": 0.0
            },
            "stream": False,
        }

        #  如果原生支持，则在调用时候直接将 tools 作为参数传入
        if self._config.supports_native_tools and self.tools:
            payload["tools"] = self.tools

        console.print(f"Chat (sync) payload: {payload}")

        try:
            uri = self._get_chat_url()
            response = self._client.post(uri, json=payload, timeout=60.0) # Add a timeout
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except httpx.RequestError as e:
            console.print(f"An error occurred while requesting {e.request.url!r}.")
            raise
        except httpx.HTTPStatusError as e:
            console.print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            console.print(f"An unexpected error occurred during sync chat: {e}")
            raise

    def batch_chat(self, batch: List[List[Message]]):
        # For batch chat, you would typically use asyncio.gather for parallel requests.
        # This is a placeholder, implementation depends on specific requirements.
        console.print("Batch chat not yet implemented for parallel processing.")
        raise NotImplementedError("Batch chat needs to be implemented using async for parallel requests.")

    def __del__(self):
        # Ensure clients are closed when the object is garbage collected
        self._client.close()
        # For async client, it's better to manage its lifecycle explicitly in async contexts,
        # but for demonstration, we can try to close it here.
        # In a real async application, you'd typically use 'async with' for the client.
        try:
            self._async_client.aclose()
        except RuntimeError:
            pass # Already closed or not initialized in an async loop

