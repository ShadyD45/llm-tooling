
# LLM Tooling Framework

A simple toy framework to enable tool usage with LLMs (like Ollama's models). It supports automatic discovery and registration of tools defined using decorators.

## Features

- Auto-discovery of tool functions (class methods or standalone)
- Decorator-based registration using `@tool_method`
- Supports structured tool calling with arguments and response parsing
- Easy integration with Ollama's chat interface

## Quickstart

### 1. Define your tools

Create tool functions in the `tools/` directory. Use the `@tool_method` decorator to register them:
For example you can define a WeatherTool api like below
```python
from main.registry.tool_registry import ToolRegistry as tools

@tools.tool_method(name="get_weather_for_location", description="Get weather for a givrn location")
def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny."
```

### 2. Initialize in your main app

Use the `LlmTooling` interface to simplify initialization and tool usage.

```python
from ollama import chat
from main import LlmTooling

# Initialize or register all tools
LlmTooling.init()

messages = [{"role": "user", "content": "What's the weather in Paris?"}]
response = chat(
    model="llama3.2:3b",
    messages=messages,
    tools=LlmTooling.get_all_tools_as_callable() # Get all available tools
)

followup = LlmTooling.parse_and_call_tool_if_available(response) # Depending on the LLM response, call the requried tool if needed 

if followup:
    # Send followup to LLM for continuation
    final_response = chat(
        model="llama3.2:3b",
        messages=followup,
        tools=LlmTooling.get_all_tools_as_callable()
    )
    print(final_response)
```

### 3. Tool Decorator API

```python
@tools.tool_method(name="tool_name", description="What the tool does")
def your_tool_function(arg1: str, arg2: int) -> str:
    return "result"
```

### 4. Examples:
- [chat_with_tool_calling](https://github.com/ShadyD45/llm-tooling/blob/main/examples/chat_with_tool_calling.py)

## Example Tool Calling Flow

- LLM chooses to call a tool (via `tool_calls` in response)
- `parse_and_call_tool_if_available` runs the function
- Result is sent back to the LLM using the appropriate message format

## Notes

- Only functions marked with `@tool_method` are registered
- Both class methods and standalone functions are supported

## License

MIT
