from main.registry.tool_registry import ToolRegistry


def main():
    ToolRegistry.register_tools()
    print(ToolRegistry.get_all_tools_as_callable())

    for tool in ToolRegistry.get_all_tools():
        print(tool)


if __name__ == '__main__':
    main()
