# WeatherApp
The WeatherApp simulates the weather conditions as described in the problem statement in WeatherData.pdf. It stores the output as "|" separated values in a text file. The app uses Google and DarkSky API's to generate locations and weather details respectively. User interaction is managed via command line, where the user can either specify samples (count) to generate or specify a csv file along with sample count. The csv file stores the city and country information separated by "," and each entry terminated by newline. Google and DarkSky API Keys are also passed in as command line arguments

The app is segregated into following modules

- conf : This holds the configuration required for the app i.e. logging
- data : This holds the input files required by the application and any processed output files
- location : Python module to fetch the coordinates i.e. longitude, latitude and elevation for a location. This module uses google API's to generate geolocation coordinates
- stats : Python module to generate the weather statistics . This module uses DarkSky API's to fetch weather statistics
- utils : Python module with basic reusable code used by other modules
- tests : Unittest code for the application
- wetahergen : Python module to generate weather samples needed for simulation module. In case of DarkSky API failure the module generates samples using either mean of existing recordset or random values.
- weathersim : Python module to simulate and store the weather samples. In case the module unable to find relevant samples in record set, it uses the similar sample generation algorithm as in weathergen module.
- main : main module to parse arguments and stich other modules together

## Dependencies 
WeatherApp requires python2.7 along with following python modules
- requests==2.21.0
- pandas==0.24.2

## Build
clone the git repository and install the python dependencies specified in the requirements.txt using pip command
```
pip install -r requirements.txt
```
## Unit test
To execute the unit tests run 
```
python -m  unittest tests.unittests
```
## usage
The code has been tested on ptyhon2.7 only. For help please run 
```
python main.py --help
```

For help regarding a specific option , specify the option followed by --help  
```
python main.py sample --help
```
For option where user enters the number of samples, please execute 
 ```
 python main.py sample <no_of_samples> <google_api_Key> <darksky_api_key>
 ```
For option where user inputs file location and samples, please execute 
 ```
  python main.py csvfile <csv_file_location> <no_of_samples> <google_api_Key> <darksky_api_key>
 ```
