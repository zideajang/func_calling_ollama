

# func_calling_ollama

`func_calling_ollama` 是一个轻量级的 Python 库，旨在简化在 Ollama 平台上运行的大型语言模型 (LLM) 进行工具调用 (Tool Calling) 的过程。

提供了从的方法来定义、注册和调用工具或函数，使 LLM 能够与现实世界互动并执行更广泛的任务。该库对于那些可能没有原生工具调用支持的模型（例如 `deepseek-coder-v2`）尤其有用，可以有效扩展它们的功能。



## 为什么工具调用很重要？

大型语言模型虽然在文本生成和理解方面非常强大，但它们天生缺乏直接与外部系统交互或执行现实世界操作的能力。工具调用弥补了这一差距，它允许 LLM：

* **访问实时信息:** 获取当前数据，如天气预报、新闻更新或股票价格。
* **与外部 API 交互:** 与搜索引擎、数据库或预订系统等各种服务集成。
* **执行代码:** 进行计算、运行脚本或与本地文件系统交互。
* **控制外部设备:** 潜在地与物联网 (IoT) 设备或其他硬件进行交互。

通过启用工具调用，LLM 变得更加通用和强大，能够处理需要其内部知识库之外的信息或操作的复杂、多步骤任务。

## 工具调用的实现方案

实现 LLM 工具调用有多种方法：

* **原生支持:** 一些先进的 LLM 经过专门训练，能够识别何时需要调用工具，并以结构化格式（例如 JSON）生成必要的函数调用。
* **提示工程 (Prompt Engineering):** 精心设计的提示可以引导 LLM 生成可被解析以识别工具调用意图和参数的文本。这通常涉及在提示中提供工具使用示例（少样本学习, Few-shot Learning）。
* **微调 (Fine-tuning):** 可以在包含工具调用场景示例的数据集上对模型进行微调，以提高其识别和生成适当函数调用的能力。
* **外部编排 (External Orchestration):** 可以使用一个单独的层或库（如 `func_calling_ollama`）来管理 LLM 和工具之间的交互。该库通常处理：
    * 向 LLM 展示可用的工具。
    * 解释 LLM 的输出以确定是否需要调用工具。
    * 提取工具名称和参数。
    * 执行工具。
    * 将工具的输出反馈给 LLM 以进行进一步处理。

`func_calling_ollama` 专注于外部编排方法，为集成 Ollama 模型的工具调用功能提供了一个轻量级且灵活的解决方案。

## `deepseek-coder-v2` 与工具调用

`deepseek-coder-v2` 是一个强大的代码生成模型。虽然它在理解和生成代码方面表现出色，但它可能不像其他一些 LLM 那样具备内置的、通用的工具调用支持。`func_calling_ollama` 通过提供一个框架来为这类模型启用工具调用，从而解决了这个问题。它通过以下方式实现：

1.  **结构化提示:** `func_calling_ollama` 可能会采用精心设计的提示，向 `deepseek-coder-v2` 展示可用的工具及其描述。这些提示引导模型生成表明希望使用特定工具以及必要参数的输出。
2.  **输出解析:** 库会解析模型的输出，寻找表示工具调用的特定模式或格式（如提供的 JSON 示例）。
3.  **工具执行与反馈:** 一旦识别出工具调用，`func_calling_ollama` 就会执行相应的函数，并将结果作为持续对话或任务的一部分反馈给 `deepseek-coder-v2`。这使得模型能够利用外部信息生成更准确、更具上下文相关性的代码或响应。

## 丰富的实例

以下是一些说明如何使用 `func_calling_ollama` 的示例：

**安装**

```python
pip install -e .
```

**快速入门 - 获取天气**

此示例演示了如何将关于天气的自然语言查询转换为结构化的工具调用。

* **输入:** `What's the weather in shenyang` (沈阳的天气怎么样？)
* **输出 (JSON):**
    ```json
    {
      "tools": {
        "tool": "get_weather",
        "tool_input": {
          "city_name": "Shenyang"
        }
      }
    }
    ```
* **执行流程:**
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
    Fetching weather for shenyang... # 正在为 shenyang 获取天气...
    Weather in shenyang: Sunny with mild temperatures. # shenyang 天气：晴朗，气温温和。
    ```
    库识别出 `get_weather` 工具并提取 "Shenyang" 作为 `city_name`。然后，它使用此输入执行 `get_weather` 函数，并将天气信息返回给用户或 LLM。

**示例 2: 简单计算**

* **输入:** "25 加 73 是多少?"
* **假设输出 (JSON):**
    ```json
    {
      "tools": {
        "tool": "calculate",
        "tool_input": {
          "expression": "25 + 73"
        }
      }
    }
    ```
* **执行流程:** 库将调用 `calculate` 工具并传入表达式，该工具将返回结果 "98"。

**示例 3: 搜索信息**

* **输入:** "帮我找找埃菲尔铁塔的信息。"
* **假设输出 (JSON):**
    ```json
    {
      "tools": {
        "tool": "search_web",
        "tool_input": {
          "query": "Eiffel Tower"
        }
      }
    }
    ```
* **执行流程:** 库将使用 `search_web` 工具执行网络搜索，并返回相关信息或链接。

这些示例突显了 `func_calling_ollama` 在处理各种类型工具调用方面的灵活性，使在 Ollama 上运行的 LLM 互动性更强、功能更强大。