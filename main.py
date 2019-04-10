import os
import json
import logging
import argparse
import logging.config
import pandas as pd
from weathergen.generator import GenerateWeather
from weathersim.simulate import SimulateWeather


def set_up_logging(log_config_file='./conf/logging.json',
                   default_level=logging.INFO
                   ):
    """
    Function to set up the logging configurations for the program.
    :param log_config_file: json config file containing logger configurations
    :param default_level: Default logging level
    :return:
    """

    if os.path.exists(log_config_file):
        with open(log_config_file, 'rt') as fin:
            logging.config.dictConfig(json.loads(fin.read()))
    else:
        logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                            level=default_level)


if __name__ == "__main__":

    # Set up the logging for the program
    set_up_logging('./conf/logging.json')
    cities = []
    samples_to_generate = 10

    # Parse command line parameters to fetch either the no of samples
    # or csv file location along with the google and dark sky API keys
    # required for coordinates abd weather information

    parser = argparse.ArgumentParser("Weather Simulator")
    subparsers = parser.add_subparsers(help="Weather Simulation parser Help", dest="cmd")
    # samples subparser and Arguments definition
    sp = subparsers.add_parser("samples", help='Samples ')
    sp.add_argument("samples", help="Number of Samples to generate should be < 1000 ")
    sp.add_argument("gapikey", help="Google API Key to fetch geo-coordinates")
    sp.add_argument("dapikey", help="DarkSky API Key to fetch ")
    # fileloc subparser and Arguments definition
    sp = subparsers.add_parser("fileloc", help="File location")
    sp.add_argument("file", help="CSV file with cities and country information ")
    sp.add_argument("gapikey", help="Google API Key to fetch geo-coordinates")
    sp.add_argument("dapikey", help="DarkSky API Key to fetch ")
    args = parser.parse_args()

    logging.info("Weather data generation starting now")

    if args.cmd == "samples":
        # Simulate the weather for 10 cities mentioned below  with total of 100 records
        cities = [("Sydney", "Australia"), ("Melbourne", "Australia"), ("Brisbane", "Australia"),
                  ("Perth", "Australia"), ("Delhi", "India"), ("Bogota", "Colombia"), ("Beijing", "China"),
                  ("Brussels", "Belgium"), ("Sofia", "Bulgaria"), ("Ottawa", "Canada")]
        samples_to_generate = args.samples

    else:
        # Simulate the weather for cities information fetched from the csv file
        with open(args.file) as fin:
            cities = [tuple(line.strip().split(",")) for line in fin]
            samples_to_generate = 10

    gw = GenerateWeather(cities, args.gapikey, args.dapikey)
    records = gw.generate_weather(samples_to_generate)

    logging.info("Weather data generation finished . Staring the simulation now")

    sim = SimulateWeather(pd.DataFrame(records))
    sim.simulate(samples_to_generate)
    sim.print_weather(**{"file": "./data/simulated_weather.txt"})
