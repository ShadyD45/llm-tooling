import pytest
from main.registry.tool_registry import ToolRegistry


# Clear registry state before each test
@pytest.fixture(autouse=True)
def clear_registry():
    ToolRegistry._tool_callables.clear()
    ToolRegistry._tool_funcname_callable_map.clear()
    ToolRegistry._toolname_callable_map.clear()
    yield
    ToolRegistry._tool_callables.clear()
    ToolRegistry._tool_funcname_callable_map.clear()
    ToolRegistry._toolname_callable_map.clear()


def test_tool_registration_and_retrieval():
    @ToolRegistry.tool_method(name="add_numbers", description="Add two numbers")
    def add(a: int, b: int) -> int:
        return a + b

    tools = ToolRegistry.get_all_tools()
    assert len(tools) == 1
    tool = tools[0]

    assert tool["name"] == "add_numbers"
    assert tool["description"] == "Add two numbers"
    assert callable(tool["callable"])
    assert tool["callable"](3, 4) == 7


def test_tool_registration_with_default_name_and_description():
    @ToolRegistry.tool_method()
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    tool = ToolRegistry.get_all_tools()[0]
    assert tool["name"] == "multiply"
    assert tool["description"] == "Multiply two numbers."
    assert tool["callable"](2, 5) == 10


def test_get_tool_by_name():
    @ToolRegistry.tool_method(name="concat_strings", description="Concatenate strings")
    def concat(a: str, b: str) -> str:
        return a + b

    func = ToolRegistry.get("concat_strings")
    assert func("hello", "world") == "helloworld"

    func_by_func_name = ToolRegistry.get("concat")
    assert func_by_func_name("foo", "bar") == "foobar"


def test_get_unregistered_tool_raises():
    with pytest.raises(ValueError, match='There is no tool "nonexistent" registered'):
        ToolRegistry.get("nonexistent")


def test_duplicate_tool_not_registered_twice():
    @ToolRegistry.tool_method(name="echo")
    def echo(msg: str) -> str:
        return msg

    # Registering again shouldn't duplicate
    @ToolRegistry.tool_method(name="echo")
    def echo(msg: str) -> str:
        return msg

    assert len(ToolRegistry.get_all_tools()) == 1
