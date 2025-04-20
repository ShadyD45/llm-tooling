from main.registry.tool_registry import ToolRegistry as tool


@tool.tool_method(
    name="read_file_at_path",
    description="Reads and returns the contents of a given file path. Takes 'path' as argument."
)
def read_file_at_path(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Error reading file: {e}"
