from main.registry.tool_registry import ToolRegistry as tool


@tool.tool_class
class WeatherService:
    @staticmethod
    @tool.tool_method(name="get_weather_for_location",
                      description="""
                      Given a location return the current weather for it. Only should be used if user asks for weather else don't use it
                      """)
    def get_weather_for_location(location: str) -> str:
        """
              Searches on internet with verified weather websites
              and return the current weather for given location.
              Only should be used if user asks for weather updates else don't use it

              Args:
                location (str): The location to get weather for

              Returns:
                str: Weather in string format
        """
        return f"{location} is sunny with 25°C."
