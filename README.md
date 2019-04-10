# weatherapp
The WeatherApp simulates the weather conditions and stores the output as "|" seperated values in a text file. The app uses google and DarkSky API's to generate weather statistics, DarkSKy API has limit of 1000 free requests per day thus randmon samples are generated after the treshold is reached. The App allows user either to specify on command line the number of samples to generate or specify a csv file along with number of samples to generate. The csv file must store the city and country information seperated by "," with each entry should be terminated by newline. 

The app is segregated into following modules

- conf : This holds the configuration required for the app i.e logging
- data : This holds the input files required by the application and any processed output files
- location : Python module to fetch the cordinates i.e longitude, latitude and elevation for a location.
- stats : Python module to generate the weather statistics
- utils : Python module with basic reusable code used by other modules
- tests : Unittest code for the application
- wetahergen : Python module to generate weather samples for simulation modeule
- weathersim : Python module to simulate and store the weather samples 
- main : main module to prase arguments and stich other modules together

## Dependencies 
weatherapp requires python2.7 along with following python modules
- requests==2.21.0
- pandas==0.24.2

## Build
clone the git repository and instsall the python dependecies specified in the requirements.txt using pip command
```
pip install -r requirements.txt
```
## Unit test
To execute the unit tests run 
```
python -m  unittest tests.unittests
```
## usage
The code has been tested on ptyhon2.7 only . For help please run 
```
python main.py --help
```

For help regarding a specific option , specify the option followed by --help  
```
python main.py sample --help
```
For option where user enters the number of samples , please execute 
 ```
 python main.py sample <no_of_samples> <google_api_Key> <darksky_api_key>
 ```
For option where user  inputs file location and samples , please execute 
 ```
  python main.py csvfile <csv_file_location> <no_of_samples> <google_api_Key> <darksky_api_key>
 ```



  



