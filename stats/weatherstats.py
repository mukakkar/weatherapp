import requests
import logging
from utils import util


class WeatherStats(object):
    """
    Class to hold weather statistics for a specific longitude and latitude
    """

    def __init__(self, longitude, latitude):
        """
        Default constructor
        :param longitude: longitude of the location
        :param latitude: latitude of the location
        """
        self.temperature = 0
        self.pressure = 0
        self.humidity = 0
        self.condition = ""
        self.longitude = longitude
        self.latitude = latitude

    def generate(self, **kwargs):

        """
        Default implementation of generate method . This method generates the weather stats such as
        temperature, humidity , pressure and condition for a specific longitude and latitude
        :param kwargs: python dictionary with longitude, latitude, elevation as keys and corresponding values
        :return:
        """
        self.temperature = kwargs.get("temperature", 0)
        self.pressure = kwargs.get("pressure", 0)
        self.humidity = kwargs.get("humidity", 0)
        self.condition = kwargs.get("condition", "")

    def get_stats(self):
        """
        Function to fetch the weather stats
        :return:
        Python tuple for weather stats (temperature, pressure , humidity , condition)
        """
        return self.temperature, self.pressure, self.humidity, self.condition


class APIWeatherStats(WeatherStats):
    """
        API implementation of WeatherStats class. It uses DarkSky API's to fetch the weather statistics
    """

    def generate(self, **kwargs):
        """
        API specific implementation of generate method. It fetches weather stats for a give latitude, longitude at
        specific time. Weather is fetched in SI units with current, hourly and flags information excluded
        :param kwargs: python dictionary with url , dark sky api key and time as key and corresponding values
        :return:
        """

        logger = logging.getLogger(__name__)
        dark_sky_uri = "{url}{key}/{lat},{lng},{time}".format(
            url=kwargs.get("url", "https://api.darksky.net/forecast/"),
            key=kwargs["key"],
            lat=self.latitude,
            lng=self.longitude,
            time=kwargs["time"]
        )

        try:
            logger.info("Fetching Weather stats for longitude={longitude}, latitude={latitude}".format(
                latitude=self.latitude,
                longitude=self.longitude
            ))
            resp = requests.get(dark_sky_uri, params={"exclude": "currently,flags,hourly", "units": "si"})
            # fetch the weather stats in daily section of json response
            weather_stats = resp.json()["daily"]["data"][0]
            tmax = weather_stats.get("temperatureHigh", 0.0)
            tmin = weather_stats.get("temperatureLow", 0.0)
            # generate stats from the raw information
            self.temperature = round((tmin + tmax) / 2, 1)
            self.humidity = int(weather_stats.get("humidity", 0) * 100)
            self.pressure = round(weather_stats.get("pressure", 0), 1)
            self.condition = util.get_condition(self.humidity, self.temperature)
            logger.info(
                "Weather stats temperature={temperature},humidity={humidity},pressure={pressure},condition={condition}"
                .format(
                    temperature= self.temperature,
                    humidity=self.humidity,
                    pressure=self.pressure,
                    condition=self.condition))

        except requests.exceptions.RequestException as ex:
            logger.info("Error while fetching coordinates from google API using default values " + ex)


