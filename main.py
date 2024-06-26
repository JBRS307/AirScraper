import requests as rq
from fetch_stations import fetch_stations
from fetch_installations import fetch_installations
from station import Station

import sys

# Function to parse command line arguments
def parse_args() -> tuple[bool, bool]:
    # work_mode is responsible for the way the program works
    # 0 is for "all at once" and 1 is for "one by one"
    # all other values are invalid
    try:
        work_mode = int(sys.argv[1])
        if work_mode != 0 and work_mode != 1:
            raise ValueError("Invalid argument!")
    except IndexError:
        work_mode = 0
    
    # to_file indicates if results should be written to file (1)
    # or be printed to stdout (0)
    # all other values are invalid
    try:
        to_file = int(sys.argv[2])
        if to_file != 0 and to_file != 1:
            raise ValueError("Invalid argument!")
    except IndexError:
        to_file = 0
    
    # return converts values to boolean
    return (bool(work_mode), bool(to_file))

# all at once work mode fetches all installations for all stations
# and then prints everything
def all_at_once(stations: list[Station]):
    for i in range(len(stations)):
        try:
            fetch_installations(stations[i])
        except rq.ConnectionError as err:
            print("Unable to connect, moving to the next station...")
            print(err, file=sys.stderr)
        except rq.HTTPError as err:
            print("HTTP error, moving to the next station...")
            print(err, file=sys.stderr)
        except rq.Timeout as err:
            print("Request timeout, moving to the next station...")
            print(err, file=sys.stderr)

# one by one work mode fetches installations for one station,
# prints it and then sets the pointer to None so garbage
# collector can delete them. After that goes to next station
def one_by_one(station: Station):
    try:
        fetch_installations(station)
    except rq.ConnectionError as err:
        print("Unable to connect, station will not be modified!")
        print(err, file=sys.stderr)
    except rq.HTTPError as err:
        print("HTTP error, station will not be modified!")
        print(err, file=sys.stderr)
    except rq.Timeout as err:
        print("Request timeout, station will not be modified!")
        print(err, file=sys.stderr)

# function to print to std, accepts list so it's universal
# (for one by one mode one element list is passed)
def print_to_std(stations: list[Station]):
    print(*stations, sep="\n")

# function to write to file, works analogically to print_to_std()
def write_to_file(stations: list[Station], open_mode: str):
    with open("stations.txt", open_mode) as fp:
        for station in stations:
            fp.write(str(station))
            fp.write('\n')


if __name__ == "__main__":
    # if work_mode is true, then one_by_one mode is active, else all_at_once
    # if to_file is true, then output is written to file, else printed to stdout
    work_mode, to_file = parse_args()

    try:
        stations = fetch_stations()
    except rq.ConnectionError as err:
        print("Unable to connect!")
        raise SystemExit(err)
    except rq.HTTPError as err:
        print("HTTP error")
        raise SystemExit(err)
    except rq.Timeout as err:
        print("Request timeout")
        raise SystemExit(err)
    
    if work_mode:
        for i in range(len(stations)):
            one_by_one(stations[i])
            if to_file:
                # file is created (or overwritten) for the first station
                # then every next station is appended to the end of file
                open_mode = 'w' if i == 0 else 'a'
                write_to_file([stations[i]], open_mode)
            else:
                print_to_std([stations[i]])
            # setting pointer to None
            stations[i].installations = None
    else:
        all_at_once(stations)
        if to_file:
            write_to_file(stations, 'w')
        else:
            print_to_std(stations)


