from installation import Installation
from station import Station
from fetch import fetch_url

PAGE_SIZE = 500

URL = "https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/" # Base URL for installations

ARG = "Lista stanowisk pomiarowych dla podanej stacji" # JSON key for installation list
ID = "Identyfikator stanowiska" # JSON key for installation id
CODE = "Wskaźnik - kod" # JSON key for param code

# Function to set fetch url, station id is rqeuired for API to work
# Arguments for page and size are also required
def set_installation_url(station_id: int, page: int, size: int) -> str:
    global URL

    if page < 0:
        raise ValueError("Page number cannot be nagative!")
    if size < 0:
        raise ValueError("Page size cannot be negative!")
    
    return URL + str(station_id) + "?page=" + str(page) + "&size=" + str(size)

# Function to fetch installations for given station
# It updates station's installations array
# Works analogically to fetch_stations()
def fetch_installations(station: Station):
    global PAGE_SIZE, ARG, ID, CODE

    url = set_installation_url(station.id, 0, PAGE_SIZE)
    res = fetch_url(url)

    res_json = res.json()
    for installation in res_json[ARG]:
        station.add_installation(Installation(int(installation[ID]), station.id, installation[CODE]))
    
    pages = int(res_json["totalPages"])

    for i in range(1, pages):
        url = set_installation_url(station.id, i, PAGE_SIZE)
        res = fetch_url(url)
        for installation in res_json[ARG]:
            station.add_installation(Installation(int(installation[ID]), station.id, installation[CODE]))


