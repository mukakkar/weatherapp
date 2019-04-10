import unittest
from location.cordinates import Coordinates
from stats.weatherstats import WeatherStats
from utils import util


class TestWeatherSim(unittest.TestCase):
    """
    Unit tests
    """

    def test_util_random_date(self):
        """
        Tests the random date generation logic . Test is marked passed if date isn't null
        :return:
        """
        date = util.gen_random_date()
        self.assertNotEqual(date, None)

    def test_get_condition(self):
        """
        Tests the condition generation logic. Test is marked passed if function logic returns Rain
        :return:
        """
        self.assertEqual(util.get_condition(90, 32), "Rain")

    def test_get_existing_random_sample_empty_records(self):
        """
        Tests the random sample generation logic. Test is marked passed if temperature, pressure and humidity
        values are not null
        :return:
        """
        self.assertNotEquals(util.get_existing_random_sample([], "Delhi", "India"), (0, 0, 0))

    def test_get_existing_random_sample_empty_records(self):
        """
        Test the mean sample generation logic. Test is marked passed if temperature, pressure and humidity
        values are mean of existing record set.
        """
        records = [{
            "city": "Delhi",
            "country": "India",
            "year": 2018,
            "month": 1,
            "day": 1,
            "latitude": 28.7040592,
            "longitude": 77.10249019999999,
            "elevation": 218.0439605712891,
            "temperature": 32,
            "humidity": 60,
            "pressure": 1013,
            "condition": "Sunny"
        }]
        self.assertEqual(util.get_existing_random_sample(records, "Delhi", "India"), (32.0, 1013.0, 60, "Sunny"))

    def test_weather_stats(self):
        """
        Tests default weather stats object. Test is marked passed if null values are returned
        :return:
        """
        ws = WeatherStats(77.10249019999999, 28.7040592)
        self.assertEqual(ws.get_stats(), (0, 0, 0, ""))

    def test_weather_stats_withinfo(self):
        """
        Tests default weather stats generation logic. Test is marked passed if same object passed as argument
        returned
        :return:
        """
        ws = WeatherStats(77.10249019999999, 28.7040592)
        ws.generate(**{
            "temperature": 32,
            "pressure": 1025,
            "humidity": 90,
            "condition": "Rain"
        })
        self.assertEqual(ws.get_stats(), (32, 1025, 90, "Rain"))

    def test_coordinates(self):
        """
        Tests default coordinates  object. Test is marked passed if null values are returned
        :return:
        """
        co = Coordinates("nocity,nocountry")
        self.assertEqual(co.get_coordinates(), (0, 0, 0))

    def test_coordinates_withinfo(self):
        """
        Tests default coordinates generation logic. Test is marked passed if same object passed as argument
        is returned
        :return:
        """

        co = Coordinates("Delhi,India")
        co.generate(**{
            "longitude": 77.10249019999999,
            "latitude": 28.7040592,
            "elevation": 218.0439605712891
        })
        self.assertEqual(co.get_coordinates(), (77.10249019999999, 28.7040592, 218.0439605712891))


if __name__ == '__main__':
    unittest.main()