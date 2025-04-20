import importlib.util
import logging as log
import os
import sys
from typing import Callable


class ToolRegistry:
    _tool_classes = []
    _tool_callables = []
    _toolname_callable_map = {}
    _tool_funcname_callable_map = {}

    _tooling_dirs = ["tools", "tooling"]

    @staticmethod
    def register_tools(tool_location: list[str] = None) -> None:
        if tool_location:
            ToolRegistry._tooling_dirs.extend(tool_location)
        ToolRegistry._tooling_dirs = list(set(ToolRegistry._tooling_dirs))  # Remove duplicates

        # Get absolute path of project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # Only consider default and provided "tool" directories under the project root
        valid_dirs = []
        for subdir in ToolRegistry._tooling_dirs:
            full_path = os.path.join(project_root, subdir)
            if os.path.isdir(full_path):
                valid_dirs.append(full_path)

        ToolRegistry._tooling_dirs = valid_dirs  # Override any previous entries

        # Register all tool classes from the specified directories
        for path in ToolRegistry._tooling_dirs:
            ToolRegistry.import_and_register_tool_classes(path)

    @staticmethod
    def import_and_register_tool_classes(path: str) -> None:
        """Recursively import all .py files from the specified directory and its subdirectories."""
        for root, _, files in os.walk(path):
            for filename in files:
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_path = os.path.join(root, filename)
                    module_name = os.path.splitext(os.path.basename(filename))[0]

                    try:
                        spec = importlib.util.spec_from_file_location(module_name, module_path)
                        module = importlib.util.module_from_spec(spec)
                        sys.modules[module_name] = module
                        spec.loader.exec_module(module)
                    except Exception as e:
                        log.warning(f"Failed to import {module_name} from {module_path}: {e}")

    @classmethod
    def tool_class(cls, klass) -> None:
        if klass not in cls._tool_classes:
            cls._tool_classes.append(klass)
        return klass

    @staticmethod
    def tool_method(name: str = None, description: str = None):
        def decorator(func: Callable):
            if (description is None and
                    func.__doc__ is None):
                log.warning(f"Method {func.__name__} marked as tool but missing description")
                #raise ValueError(f"Method {func.__name__} marked as tool but missing description")

            func._is_tool = True
            func._tool_name = name or func.__name__
            func._tool_description = description or func.__doc__

            if (func not in ToolRegistry._tool_callables and
                    (func.__name__ not in ToolRegistry._tool_funcname_callable_map.keys() or
                     func._tool_name not in ToolRegistry._toolname_callable_map.keys())
            ):
                ToolRegistry._tool_callables.append(func)
                ToolRegistry._tool_funcname_callable_map[func.__name__] = func
                ToolRegistry._toolname_callable_map[func._tool_name] = func

            return func

        return decorator

    @classmethod
    def get_all_tools(cls) -> list[callable]:
        tools = []

        for method in cls._tool_callables:
            if getattr(method, "_is_tool", False):
                tools.append({
                    "callable": method,
                    "name": method._tool_name,
                    "description": method._tool_description,
                })

        return tools

    @classmethod
    def get_all_tools_as_callable(cls) -> list[Callable]:
        return cls._tool_callables

    @staticmethod
    def get(item: str) -> Callable:
        if item in ToolRegistry._toolname_callable_map.keys():
            return ToolRegistry._toolname_callable_map.get(item)
        elif item in ToolRegistry._tool_funcname_callable_map.keys():
            return ToolRegistry._tool_funcname_callable_map.get(item)
        else:
            raise ValueError(f"There is no tool \"{item}\" registered")
