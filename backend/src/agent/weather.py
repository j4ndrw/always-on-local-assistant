from .error import agent_tool_error
from ..settings.settings import settings
from .agent import Toolkit, create_tool_handlers, create_tool_repository
import requests


def get_weather() -> dict:
    """
    Gets the weather, given the user's position.

    Returns:
        dict: API response from Open Meteo that contains various data that needs to be interpreted.
    """
    gps_position = settings.metadata.get("gpsPosition")
    if gps_position is None:
        return agent_tool_error(get_weather.__name__, message="Could not determine weather - no GPS position was found on the user's device.")

    latitude = gps_position.get("latitude")
    longitude = gps_position.get("longitude")
    if latitude is None or longitude is None:
        return agent_tool_error(get_weather.__name__, message="Could not determine weather - no latitude/longitude was found on the user's device.")

    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude:.2f}&longitude={longitude:.2f}&daily=precipitation_sum,sunrise,sunset,precipitation_hours,temperature_2m_min,temperature_2m_max&timezone=auto&current=temperature_2m,precipitation,is_day")
    return response.json()

_repository = create_tool_repository(get_weather)
_handlers = create_tool_handlers(lambda _: {
    get_weather: [],
})

weather_toolkit = Toolkit(repository=_repository, handlers=_handlers)
