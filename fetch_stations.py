from station import Station
from fetch import fetch_url

# Stores maximum page size available at api request (we want big pages
# because we want to fetch info about all stations
PAGE_SIZE = 500

# Base URL for stations API
URL = "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll"

ARG = "Lista stacji pomiarowych" # JSON key for station list
ID = "Identyfikator stacji" # JSON key for station ID
NAME = "Nazwa stacji" # JSON key for station name

# Function to modify base url to get maximum number of stations
# on one page and to change the page
def set_stations_url(page: int, size: int) -> str:
    global URL

    if page < 0:
        raise ValueError("Page number cannot be nagative!")
    if size < 0:
        raise ValueError("Page size cannot be negative!")
    
    return URL + "?page=" + str(page) + "&size=" + str(size)


# Main fetch function for stations
def fetch_stations() -> list[Station]:
    global PAGE_SIZE, ARG, ID, NAME

    url = set_stations_url(0, PAGE_SIZE)

    res = fetch_url(url)
    
    stations = []
    res_json = res.json() # Variable to avoid multiple calls
    for station in res_json[ARG]:
        stations.append(Station(int(station[ID]), station[NAME]))
    
    pages = int(res_json["totalPages"])
    
    # In case when stations don't fit on a single page
    for i in range(1, pages):
        url = set_stations_url(i, PAGE_SIZE)
        res = fetch_url(url)
        for station in res.json()[ARG]:
            stations.append(Station(int(station[ID]), station(NAME)))
    
    return stations

