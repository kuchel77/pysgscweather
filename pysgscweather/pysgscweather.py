""" Interact with the Healthcheck.io website """
import logging
import asyncio
import socket
import aiohttp
import async_timeout
import json

_LOGGER = logging.getLogger(__name__)

class WeatherData():
    """ Interact with the Healthcheck.io website """
    def __init__(self, loop=None, weather_url=None, session=None):
        _LOGGER.debug("pysgscweather initializing new server at: %s", weather_url)
        self._weather_url = weather_url
        self._loop = loop
        self._session = session
        self._results = False
        self._text = None
        self._airtemp = None
        self._windspeed = None
        self._timestamp = None
        self._atmosphericpressure = None
        self._winddirection = None
        self._winddirectioncompass = None
        self._vapourpressure = None
        self._solar = None
        self._gustspeed = None
        self._relativehumidity = None
        self._location = None

    def update_url(self, weather_url=None):
        """ Update the url """
        self._weather_url = weather_url

    def status(self):
        return self._results


    def windspeed(self):
        return self._windspeed

    def airtemp(self):
        return self._airtemp

    def timestamp(self):
        return self._timestamp
        
    def atmosphericpressure(self):
        return self._atmosphericpressure
        
    def winddirection(self):
        return self._winddirection
        
    def windcompassdirection(self):
        return self._winddirectioncompass
        
    def vapourpressure(self):
        return self._vapourpressure
        
    def solar(self):
        return self._solar
        
    def gustspeed(self):
        return self._gustspeed
        
    def relativehumidity(self):
        return self._relativehumidity
        
    def location(self):
        return self._location

    async def update_data(self):
        """ Sends the request """
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                response = await self._session.get(url=self._weather_url, ssl=False)
                try:
                    if response.status in [200]:
                        self._results = True
                        self._json = await response.json() 

                        self._gustspeed = self._json["records"][0]["fields"]["gustspeed"]
                        self._airtemp = self._json["records"][0]["fields"]["airtemp"]
                        self._windspeed = self._json["records"][0]["fields"]["windspeed"]
                        self._timestamp = self._json["records"][0]["fields"]["time"]
                        self._atmosphericpressure = self._json["records"][0]["fields"]["atmosphericpressure"]
                        self._winddirection = self._json["records"][0]["fields"]["winddirection"]
                        self._winddirectioncompass = self._json["records"][0]["fields"]["windcompassdirection"]
                        self._vapourpressure = self._json["records"][0]["fields"]["vapourpressure"]
                        self._solar = self._json["records"][0]["fields"]["solar"]
                        self._relativehumidity = self._json["records"][0]["fields"]["relativehumidity"]
                        self._location = self._json["records"][0]["fields"]["location"]
                    else:
                        _LOGGER.error(
                            "Error code %s - %s",
                            response.status,
                            response.text,
                        )
                        return None
                except (TypeError, KeyError) as error:
                    _LOGGER.error("Error parsing data from connectgh, %s", error)
                    return None

        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error("Error connecting to ConnectGH, %s", error)
            return None

        return self._results
