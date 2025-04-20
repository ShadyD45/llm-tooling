from main.registry.tool_registry import ToolRegistry as tool


@tool.tool_method(name="add_numbers", description="Add two numbers together.")
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers. Only should be used if user wants to perform mathematical operations

    Args:
      a (int): The first number
      b (int): The second number

    Returns:
      int: The sum of the two numbers
    """
    # The cast is necessary as returned tool call arguments don't always conform exactly to schema
    # E.g. this would prevent "what is 30 + 12" to produce '3012' instead of 42
    return int(a) + int(b)
