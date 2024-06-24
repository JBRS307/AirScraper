import requests as rq
from fetch_stations import fetch_stations

if __name__ == "__main__":
    try:
        stations = fetch_stations()
    except rq.ConnectionError:
        print("Unable to connect!")
        exit(1)
    
    print(*stations)
