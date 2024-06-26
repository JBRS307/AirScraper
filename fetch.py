import requests as rq
from time import sleep

# Wrapper function for fetching.
def fetch_url(url: str) -> rq.Response:
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