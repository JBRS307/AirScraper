import requests as rq
from station import Station
from time import sleep

# Stores maximum page size available at api request (we want big pages
# because we want to fetch info about all stations
PAGE_SIZE = 500

# Base URL for stations API
STATIONS_URL = "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll"

STATIONS_ARG = "Lista stacji pomiarowych" # JSON key for station list
STATION_ID = "Identyfikator stacji" # JSON key for station ID
STATION_NAME = "Nazwa stacji" # JSON key for station name

# Function to modify base url to get maximum number of stations
# on one page and to change the page
def set_stations_url(page: int, size: int) -> str:
    global STATIONS_URL

    if page < 0:
        raise ValueError("Page number cannot be nagative!")
    if size < 0:
        raise ValueError("Page size cannot be negative!")
    
    return STATIONS_URL + "?page=" + str(page) + "&size=" + str(size)


# Wrapper function for fetching.
def fetch_url(url) -> rq.Response:
    while True:
        res = rq.get(url)

        # Response status codes that we need to care about are 200 (Success) and
        # 429 (Too many requests), if any other code occurs we raise an exception
        if res.status_code != 200 and res.status_code != 429:
            raise rq.RequestException("Request failed with code: " + str(res.status_code))
        
        # In case of too frequent requests we're gonna have to wait some time
        if res.status_code == 429:
            print("Too many requests, waiting 30 seconds for next request...")
            sleep(30)
        else:
            return res

# Main fetch function for stations
def fetch_stations() -> list[Station]:
    global PAGE_SIZE, STATIONS_ARG, STATION_ID, STATION_NAME

    url = set_stations_url(0, PAGE_SIZE)

    res = fetch_url(url)
    
    stations = []
    res_json = res.json() # Variable to avoid multiple calls
    for station in res_json[STATIONS_ARG]:
        stations.append(Station(int(station[STATION_ID]), station[STATION_NAME]))
    
    pages = int(res_json["totalPages"])
    
    # In case when stations don't fit on a single page
    for i in range(1, pages):
        url = set_stations_url(i, PAGE_SIZE)
        res = fetch_url(url)
        for station in res.json()[STATIONS_ARG]:
            stations.append(Station(int(station[STATION_ID]), station(STATION_NAME)))
    
    return stations

