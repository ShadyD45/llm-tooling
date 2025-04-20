from ollama import ChatResponse
from main.registry.tool_registry import ToolRegistry as tools


class LlmTooling:
    @staticmethod
    def init():
        tools.register_tools()

    @staticmethod
    def get_all_tools_as_callable() -> list[callable]:
        return tools.get_all_tools_as_callable()

    @staticmethod
    def parse_and_call_tool_if_available(response: ChatResponse) -> list[dict]:
        if not response.message.tool_calls:
            return []

        followups = []

        for call in response["message"]["tool_calls"]:
            func_name = call.function.name
            args = call.function.arguments

            try:
                func = tools.get(func_name)
            except ValueError:
                followups.append(response.message)
                followups.append({'role': 'tool',
                                  'content': f"""
                                        No tool registered with name: {func_name}, Answer with your whatever knowledge you have
                                  """,
                                  'name': func_name})
                return followups

            if not func:
                print(f"No tool registered with name: {func_name}")
                continue

            print(f"Calling tool {func_name}")
            result = func(**args)

            # Only needed to chat with the model using the tool call results
            if response.message.tool_calls:
                # Add the function response to messages for the model to use
                followups.append(response.message)
                followups.append({'role': 'tool', 'content': str(result), 'name': func_name})

            # print(f"Tool {func_name} returned: {result}")

        # print(f"followup: {followups}")

        return followups
