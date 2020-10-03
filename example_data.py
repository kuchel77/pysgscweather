"""Example usage of pysgscweather."""
import asyncio
import aiohttp
from pysgscweather import pysgscweather


async def example():
    """Get pending packages."""
    async with aiohttp.ClientSession() as session:
        weatherdata = pysgscweather.WeatherData(
            LOOP,
            weather_url="https://www.connectgh.com.au/api/records/1.0/search/?dataset=weather-stations&q=&rows=1&sort=eventid&refine.location=Hamilton",
            session=session
        )

        result = await weatherdata.update_data()
        print("Result ", result)
        print(weatherdata.airtemp())


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(example())
