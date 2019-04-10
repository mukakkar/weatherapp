import logging
import random
from location.cordinates import APICoordinates
from stats.weatherstats import APIWeatherStats
import utils.util as util
logger = logging.getLogger(__name__)


class GenerateWeather(object):
    """
        Class to generate the weather samples. This information is required by the simulator module
    """

    def __init__(self, cities, api_key_google, api_key_dark_sky):

        """

        :param cities: list of cities to generate the weather information for
        :param api_key_google: google API key
        :param api_key_dark_sky: DarkSky API Key
        """
        self.cities = cities
        self.api_key_google = api_key_google
        self.api_key_dark_sky = api_key_dark_sky

    def generate_weather(self, samples_to_generate):
        """

        :return: simulated weather details in a python list with each element as a python dictionary
        """
        rows = []
        for i in range(samples_to_generate):

            # Select a random city from the cities list
            city, country = self.cities[random.randint(0, len(self.cities))]
            coordinates = APICoordinates(",".join([city, country]))
            coordinates.generate(**{
                "url": "https://maps.googleapis.com/maps/api/geocode/json",
                "url2": "https://maps.googleapis.com/maps/api/elevation/json",
                "key": self.api_key_google
            })
            longitude, latitude, elevation = coordinates.get_coordinates()

            # DarkSky API only provides 1000 free API calls per day, in case it's not feasible to get the sample data
            # from API generate random samples
            date = util.gen_random_date()
            stats = APIWeatherStats(longitude, latitude)
            stats.generate(**{
                "key": self.api_key_dark_sky,
                "url": "https://api.darksky.net/forecast/",
                "time": date.strftime("%s")
            })
            temperature, humidity, pressure, condition = stats.get_stats()

            if (temperature, humidity, pressure) == (0, 0, 0):
                # unable to fetch Data from API generate random values
                temperature, pressure, humidity, condition = util.get_random_sample(rows, city, country)

            logger.info("""location={location},year={year},month={month},day={day}, latitude={latitude},
            longitude={longitude},elevation={elevation},temperature={temperature},humidity={humidity}, 
            pressure={pressure}, condition={condition}""".
                        format(location=city,
                               year=date.year,
                               month=date.month,
                               day=date.day,
                               latitude=latitude,
                               longitude=longitude,
                               elevation=elevation,
                               temperature=temperature,
                               humidity=humidity,
                               pressure=pressure,
                               condition=condition
                               ))
            # append the weather information to the list
            rows.append({
                    "city": city,
                    "year": date.year,
                    "month":  date.month,
                    "day":  date.day,
                    "latitude": latitude,
                    "longitude": longitude,
                    "elevation": elevation,
                    "temperature": temperature,
                    "humidity": humidity,
                    "pressure": pressure,
                    "condition": condition
             })

        return rows
