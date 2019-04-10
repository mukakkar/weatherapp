import requests
import logging


class Coordinates(object):
    """
        Default implementation of coordinates class. This class stores the latitude
     """
    def __init__(self, location):
        """
          Default constructor
        :param location: location in city,country format i.e Sydney,Australia
        """

        self.longitude = 0
        self.latitude = 0
        self.elevation = 0
        self.location = location


    def generate(self, **kwargs):

        """
        Default implementation of generate method . It expects a dictionary with
        longitude, latitude, elevation as keys and corresponding values
        :param kwargs:
        :return:
        """

        self.longitude = kwargs.get("longitude", 0)
        self.latitude = kwargs.get("latitude", 0)
        self.elevation = kwargs.get("elevation", 0)

    def get_coordinates(self):
        """
        Function to return the coordinates as python tuple
        :return: longitude, latitude and elevation
        """
        return self.longitude, self.latitude, self.elevation


class APICoordinates(Coordinates):
    """
        Extension of Coordinates class to fetch the coordinates via API
    """

    def generate(self, **kwargs):

        """
        Override the default implementation to generate the coordinates using API calls
        This implementation uses google API to fetch the coordinates . Coordinates  are stored as
        class attributes after fetching
        :param kwargs: python dictionary with url's to fetch coordinates and the API Key
        :return:
        """
        logger = logging.getLogger(__name__)
        try:
            # Fetch longitude and latitude
            logger.info("Fetching longitude and latitude for location={location}".format(location=self.location))
            resp = requests.get(
                kwargs.get("url", "https://maps.googleapis.com/maps/api/geocode/json"),
                params={"address": self.location, "key": kwargs["key"]}
            )
            respj = resp.json()
            # Fetch the latitude and longitude from the response
            self.longitude = respj["results"][0]["geometry"]["location"]["lng"]
            self.latitude = respj["results"][0]["geometry"]["location"]["lat"]
            logger.info(
                "Fetched coordinates are latitude={latitude}, longitude={longitude}".format(
                    longitude=self.longitude,
                    latitude=self.latitude))

            logger.info("Fetching elevation for location={location}".format(location=self.location))
            resp = requests.get(
                kwargs.get("url2", "https://maps.googleapis.com/maps/api/elevation/json"),
                params={"locations": "{lat},{lng}".format(lat=self.latitude, lng=self.longitude),
                        "key": kwargs["key"]
                        }
            )
            respj = resp.json()
            # Fetch the elevation
            self.elevation = respj['results'][0]['elevation']
            logger.info("Fetched elevation is {elevation} ".format(elevation=self.elevation))

        except requests.exceptions.RequestException as ex:
            logger.info("Error while fetching coordinates from google API using default values " + ex)
