# Data Scraper

Simple data scraper that can be used to fetch basic stations and installations info for *Jakość Powietrza GIOŚ* API.

To install use:
```shell
git clone https://github.com/JBRS307/AirScraper.git
```

To work, script requires additional module `requests`, to install it use
```shell
pip install -r requirements.txt
```

To run the program:
```shell
python3 main.py
```

Program can work in two modes:
- *all at once* - fetch all installations for all stations first and then print the output. This worke mode is the default one.
- *one by one* - fetch installations for one station, print it, free memory taken by installations array and proceed to the next station. This one is slower, but requires less memory.

To choose work mode use
```shell
python3 main.py [WORK_MODE_NUMBER]
```
where **0** is for *all at once mode* and **1** is for *one by one mode*

There are to options to get the output:
- print to `stdout` - this is the default option
- write to `stations.txt` file

To choose print mode use:
```shell
python3 main.py <WORK_MODE_NUMBER> [PRINT_MODE_NUMBER]
```
where **0** is for printing to `stdout` and **1** is for writing to file.   
WARNING: In order to specify printing mode, work mode must be specified.

Any argument other than **0** or **1** will throw exception in both cases.

Example:
```shell
python3 main.py 0 1
```
Program works in *all at once* mode with output written to file.

---
## Classes

### Station

Class fields:
- `id` - contains station id
- `name` - contains station name
- `installations` - contains list of `Installation` objects that correspond to the station's installations

Methods:
- `__init__(id, name, installations=None)` - constructor
- `__str__()` - converts class to string with the following format:  
*Station #1: (Station name):*  
*installation #0: 'PM10'*
*installation #2: 'NO2'*
*---*
- `add_installation(installation)` - adds installation to `installations` list

To import class use:
```py3
from station import Station
```

### Installation

Class fields:
- `id` - installation id
- `station_id` - id of station where installation is placed
- `param_code` - code of air parameter that installation measures

Methods:
- `__init__(id, station_id, param_code)` - constructor
- `__str__()` - converts class to string with the following format:  
*installation #0: 'PM10'*

To import class use:
```py3
from installation import Installation
```

---

## Modules

### fetch_stations

Module to fetch all the stations from the API.

Contains only one public function

```py3
def fetch_stations() -> list[Station]
```
Returns the list of `Station` objects.

To import use:
```py3
from fetch_stations import fetch_stations
```

### fetch_installations

Module to fetch all installations for given station

```py3
def fetch_installations(station: Station)
```
Modifies `Stations` object's `installations` list. Adds all found installations.

To import use:
```py3
from fetch_installations import fetch_installations
```







