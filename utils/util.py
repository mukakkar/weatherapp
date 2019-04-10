import datetime
import random
import logging

logger = logging.getLogger(__name__)


def gen_random_date():
    """
    function to generate random epoch time stamp . The time is generated between now and past 5 years
    :return:
    Return the python datetime object
    """

    epoch_now = int(datetime.datetime.now().strftime("%s"))
    epoch_prev = epoch_now - (24 * 3600 * 365 * 5)

    # generate a random integer between now and now - 5 years and convert it into python date
    return datetime.datetime.fromtimestamp(
        random.randint(epoch_prev, epoch_now)
    )


def get_condition(humidity, temperature):
    """
    Function to calculate the condition from humidity and temperature
    :param humidity: Atmospheric Humidity
    :param temperature: Atmospheric Pressure
    :return:
    """

    if (humidity > 80) & (temperature > 0):
        condition = "Rain"
    elif (humidity > 70) & (temperature < 0):
        condition = "Snow"
    else:
        condition = "Sunny"

    return condition


def get_existing_random_sample(records, city, country):

    """
    Function to generate a random sample based upon the  records already available in the list .
    The function filters all the records pertaining to the specified city anc country and takes
    average of all the records . In case records aren't available a random sample is generated

    :param records: python list of existing weather information for the location
    :param city: city for which weather sample is requested
    :param country: country for which weather sample is requested
    :return:
    Returns a python tuple containing temperature , pressure , humidity and condition
    """

    temperature = 0
    pressure = 0
    humidity = 0

    # Fetch the records for the specific city and country
    filtered_records = filter(lambda r: r["city"] == city and r["country"] == country, records)
    if len(filtered_records):
        # generate the weather sample as mean of existing statistics
        for record in filtered_records:
            temperature = temperature + record["temperature"]
            humidity = humidity + record["humidity"]
            pressure = pressure + record["pressure"]

        temperature = round(float(temperature) / len(filtered_records), 1)
        humidity = int((float(humidity) / len(filtered_records)))
        pressure = round(float(pressure) / len(filtered_records), 1)
    else:
        # genera the random sample
        temperature = random.randint(-30, 40)
        pressure = random.randint(1050, 1085)
        humidity = random.randint(30, 90)

    condition = get_condition(humidity, temperature)

    return temperature, pressure, humidity, condition
