#! python3
""" spring 2021
Prints the current weather for my location. """
import sys
import json
import pathlib
import requests
import datetime

USAGE = f"USAGE: python3 {sys.argv[0]} apikey"

# weatherbit:
url = "https://api.weatherbit.io/v2.0/current"
location = "515012"
if len(sys.argv) == 2:
    apikey = sys.argv[1]
else:
    print(USAGE)
    sys.exit(0)


# check if data file exists in folder;
# check file lifetime;
info = None
request = False
filename = pathlib.Path("weatherbit.json")

if filename.exists():
    file_mtime = filename.stat().st_mtime
    file_mtime = datetime.datetime.fromtimestamp(file_mtime)
    lifetime = file_mtime + datetime.timedelta(hours=10)
    if datetime.datetime.now() < lifetime:
        print("Last request less than 10 hours.")
        with open("weatherbit.json") as file:
            data = json.loads(
                json.load(file)
            )
            info = data['data'][0]
    else:
        request = True
else:
    request = True

# request json;
if request is True:
    try:
        answer = requests.get(
            url=url, params=dict(city_id=location, key=apikey)
        )
        answer.raise_for_status()
        with open("weatherbit.json", 'w') as write_file:
            json.dump(answer.text, write_file)
        data = json.loads(answer.text)
        info = data['data'][0]
        print("New json data requested.")
    except OSError as error:
        print("ERROR.", error)
        sys.exit(1)
    except Exception as alert:
        print("ALERT.", alert)
        sys.exit(2)

# format;
location = f"{info['timezone']}, {location}; {info['city_name']}."
date = f"Request time: {info['ob_time']}"
temperature = f"Temperature: {info['temp']}"
apparent = f"Feels like: {info['app_temp']}"
wind_direction = f"Wind direction: {info['wind_cdir_full']}"

ws = info['wind_spd']
if ws <= 1.5:
    text = "calm "
elif ws <= 5:
    text = "light breeze "
elif ws <= 9:
    text = "moderate breeze "
elif ws <= 12:
    text = "wind "
elif ws <= 16:
    text = "moderate wind "
elif ws <= 18:
    text = "STRONG WIND "
elif ws <= 20:
    text = "STORM WIND! "
else:
    text = "DON'T LEAVE THE ROOM!!! "
ws = text + format(ws, '.1f')
wind_speed = f"Wind speed: {ws}"

uvi = info['uv']
if uvi <= 2:
    uvi = "green"
elif uvi <= 5:
    uvi = "yellow..."
elif uvi <= 7:
    uvi = "orange!"
elif uvi <= 10:
    uvi = "RED!!!"
else:
    uvi = "DON'T LEAVE THE ROOM!!!"
uv_index = f"UV Index: {uvi}"

epa = info['aqi']
if epa <= 50:
    epa = "good green air."
elif epa <= 100:
    epa = "yellow moderate pollute."
elif epa <= 150:
    epa = "orange unhealthy pollution!"
elif epa <= 200:
    epa = "RED HIGH POLLUTION!"
elif epa <= 300:
    epa = "PURPLE VERY UNHEALTHY EMISSIONS!"
else:
    epa = "MAROON HAZARDOUS!!!"
air_quality = f"Air Quality: {epa}"

output = [location, date, temperature, apparent, wind_direction,
          wind_speed, uv_index, air_quality]

# output.
print(*output, sep='\n')
sys.exit(0)
