import utils.util as util
import random
import pandas as pd


class SimulateWeather(object):
    """
    Class to simulate wetaher
    """
    def __init__(self, df):
        """
        Default constructor
        :param df: pandas data frame holding generated weather information
        """
        self.df = df
        # Pandas data frame holding simulated weather information
        self.df_simulated_weather = None

    def simulate(self, samples_to_generate=10):

        # list to hold intermediate weather stats
        rows = []
        # cities information fetched from data frame
        cities_info = [self.df.loc[self.df["city"] == city,
                                    ["city", "country", "latitude", "longitude", "elevation"]].values[0]
                       for city in self.df['city'].unique()]

        for i in range(samples_to_generate):

            # fetch coordinates and country information
            city, country, latitude, longitude, elevation = cities_info[random.randint(0, len(cities_info))]
            # generate a random date and fetch records
            date = util.gen_random_date()
            df_matching_records = self.df.loc[
                (self.df["city"] == city) & (self.df["month"] == date.month)]

            # generate random sample if matching records aren't found
            if not len(df_matching_records):
                temperature, pressure, humidity, condition = util.get_random_sample(rows, city, country)
            else:
                # generate the weather as mean of existing values
                temperature = df_matching_records["temperature"].mean()
                pressure = df_matching_records["pressure"].mean()
                humidity = df_matching_records["humidity"].mean()
                condition = util.get_condition(humidity, temperature)

            rows.append({
                "city": city,
                "country": country,
                "position": "{latitude},{longitude},{elevation}".format(
                    latitude=latitude,
                    longitude=longitude,
                    elevation=elevation
                ),
                "localtime": date.isoformat(),
                "condition": condition,
                "temperature": temperature,
                "pressure": pressure,
                "humidity": humidity
            })

        # generate the simulated weather panda data frame
        self.df_simulated_weather = pd.DataFrame(rows)

    def print_weather(self, **kwargs):
        """
        function to print the weather output with values separated by | symbol
        override this function if you wish to print the output to DB or API end point
        :param kwrags: Python dictionary holding the file location as key, value pair
        :return:
        """
        columns = ["city", "position", "localtime", "condition", "temperature", "pressure", "humidity"]

        with open(kwargs["file"], "w") as fout:
            for indx, row in self.df_simulated_weather.iterrows():
                fout.write("|".join([str(row[column]) for column in columns]) + "\n")