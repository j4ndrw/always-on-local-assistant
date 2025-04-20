import requests

from src.agent.tools.tools import define_toolkit, description
from src.settings.settings import settings

_, resource, register_toolkit = define_toolkit()


@resource.create(
    description=description(
        """
        Gets the weather, given the user's position.
        """,
        returns=[
            (
                "dict",
                "API response from Open Meteo that contains various data that needs to be interpreted.",
            )
        ],
    )
)
def get_weather() -> dict:
    gps_position = settings.metadata.get("gpsPosition")
    if gps_position is None:
        return resource.error(
            get_weather.__name__,
            error="Could not determine weather - no GPS position was found on the user's device.",
        )

    latitude = gps_position.get("latitude")
    longitude = gps_position.get("longitude")
    if latitude is None or longitude is None:
        return resource.error(
            get_weather.__name__,
            error="Could not determine weather - no latitude/longitude was found on the user's device.",
        )

    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude:.2f}&longitude={longitude:.2f}&daily=precipitation_sum,sunrise,sunset,precipitation_hours,temperature_2m_min,temperature_2m_max&timezone=auto&current=temperature_2m,precipitation,is_day"
    )
    return response.json()
