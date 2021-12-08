#!/path/to/project/venv/bin/python
"""
VERSION 1.5 2021.07
Request weather forecast via api;
processes and outputs to the terminal, or sends to email.
Example:
    Alerts:
    ~16:00~~: very hot
    ~17:00~~: very hot
    tomorrow: very hot

    Weather Forecast:
    #TIME     TMP/FL   CLDS:PoP   WIND <      SPEED      <<   GUST    PRESSURE        UVI        AIR QUALITY
    *16:00  = 34°/33°  094%:000%   ENE <   l-breeze 2m/s <<   6m/s    norm 746mmHg    green 2    green air 47
    *17:00  = 34°/33°  045%:000%   ENE <   l-breeze 2m/s <<   5m/s    norm 746mmHg    green 2    green air 46
    tomorrow= 34°/33°  055%:000%   ESE <   l-breeze 2m/s <<   5m/s    norm 744mmHg   yellow 5    green air 47

Designed to run from a bash script on schedule twice a day.
Designed for the presence of api-key, gmail account and gmail password in 
byte files, encrypted in base64, in the '/%user home%/.local/bin/data'.
"""
import sys
import time
import json
import base64
import logging
import pathlib
import smtplib
import requests
import datetime


USAGE = """USAGE:
python3 weather.py              for print mode or
python3 weather.py -r/--mail    for remote mode"""

script_data_files = str(pathlib.Path.home()) + "/.local/bin/data"

LOG_FILE = f"{script_data_files}/log.txt"
LOG_MAX_BYTES = 1000000

# hours parameters
UPDATE_TIME = 4
MORNING = 7
EVENING = 17
NIGHT = 23
TOMORROW = 13

# weatherbit parameters
LOCATION = '515012'
URL_FORECASTS = "https://api.weatherbit.io/v2.0/forecast/hourly"
URL_AIRQUALITY = "https://api.weatherbit.io/v2.0/forecast/airquality"
FILE_FORECASTS = pathlib.Path(f"{script_data_files}/forecasts.json")
FILE_AIRQUALITY = pathlib.Path(f"{script_data_files}/airquality.json")
WEATHERBIT_APIKEY = f"{script_data_files}/apikey"

# gmail parameters
GMAIL_SMTP = 'smtp.gmail.com'
GMAIL_SMTP_PORT = 587
GMAIL_ACCOUNT = f"{script_data_files}/gmailaccount"
GMAIL_APP_PASSWORD = f"{script_data_files}/gmailpassword"

# weather categories (low, high) borders
BEAUFORT_SCALE = {
    'calm': (0, 0.5), 'light air': (0.6, 1.5), 'l-breeze': (1.6, 3.3), 
    'g-breeze': (3.4, 5.5), 'm-breeze': (5.6, 7.9), 'f-breeze': (8, 10.7), 
    's-breeze': (10.8, 13.8), 'wind': (13.9, 17.1), 'GALE': (17.2, 20.7),
    'S-GALE': (20.8, 24.4), 'STORM': (24.5, 28.4), 'H-STORM': (28.5, 32.6), 
    'HURRICANE': (32.7, 100)
}
AIR_QUALITY_EPA = {
    'green air': (0, 50), 'moderate': (51, 100), 'unhealthy': (101, 150),
    'EMISSIONS': (151, 200), 'VERY HIGH': (201, 300), '!HAZARDOUS!': (301, 999)
}
UV_INDEX = {
    'green': (0, 2), 'yellow': (3, 5), 'orange': (6, 7), 'RED': (8, 10), 'VIOLET': (11, 99)
}
ATMOSPHERIC_PRESSURE = {'normal': (740, 765)}

# alerts boundaries
ALERT_TEMPERATURE = (-20, 30)
ALERT_PRECIPITATION = (40, 80)
ALERT_WIND_SPEED = (18, 24)
ALERT_ULTRAVIOLET = (7, 10)
ALERT_AIR_QUALITY = (100, 200)

# output text formats
W_TIME = 10
W_TEMP = 3
W_CLD = 4
W_WIND = 6
W_SPEED = 15
W_GUST = 6
W_AP = 13
W_UV = 9
W_AQI = 15


class JSONRequestError(Exception): pass
class JSONLoadsError(Exception): pass
class SendMailError(Exception): pass


def main():
    logfile = pathlib.Path(LOG_FILE)
    if logfile.exists() and logfile.stat().st_size < LOG_MAX_BYTES:
        log_mode = 'a'
    else:
        log_mode = 'w'
    logging.basicConfig(filename=LOG_FILE, filemode=log_mode, level=logging.INFO,
                        format="%(asctime)s — %(levelname)s: [[ %(message)s ]]")
    logging.info("Start")

    if len(sys.argv) == 1:
        mode = 'LOCAL'
    elif sys.argv[1] in ['-r', '--mail']:
        mode = 'REMOTE'
    else:
        print(USAGE)
        logging.info("printing usage help.")
        sys.exit(1)
    logging.info(f"operating mode {mode}")

    requests_json = weather_files_check()
    try:
        if requests_json:
            info = request_weather_data()
            logging.info("new json data requested")

        else:
            logging.info(f"last request less than {UPDATE_TIME} hours")
            info = loads_weather_data()
            logging.info(f"OK loads")

        if not info[0] or not info[1]:
            raise JSONLoadsError("something went wrong on the way...")

    except JSONRequestError or JSONLoadsError:
        logging.exception("JSON")
        sys.exit(2)

    info = preprocess(info)
    logging.info("OK data preprocess")

    forecast_text = format_weather(info)
    logging.info("OK forecast text format")

    output_text = check_alerts(forecast_text, info)
    logging.info("OK alerts check")

    if mode == 'REMOTE':
        try:
            send_email(output_text)
        except SendMailError:
            logging.exception("send email")
            sys.exit(3)
        else:
            logging.info("send email successfully!")

    elif mode == 'LOCAL':
        print(output_text)
        logging.info("output to terminal")

    logging.info("End.")
    sys.exit(0)


def weather_files_check():
    """ Check if weather files exists in folder; check files lifetime. :return: bool """

    requests_json = False
    lifetime = datetime.timedelta(hours=UPDATE_TIME)
    for datafile in (FILE_FORECASTS, FILE_AIRQUALITY):
        if not datafile.exists():
            requests_json = True
            break

        mod_date = datetime.datetime.fromtimestamp(
            datafile.stat().st_mtime
        )
        if (datetime.datetime.now() - mod_date) > lifetime:
            requests_json = True
            break

    return requests_json


def request_weather_data():
    """ :return: tuple(list, list) """
    
    info_weather = None
    info_airquality = None
    sources = ((URL_FORECASTS, FILE_FORECASTS), (URL_AIRQUALITY, FILE_AIRQUALITY))

    try:
        with open(WEATHERBIT_APIKEY, 'br') as apifile:
            apikey = base64.b64decode(apifile.read())

        for url, datafile in sources:
            answer = requests.get(
                url=url, params=dict(city_id=LOCATION, key=apikey.decode('UTF-8'))
            )
            answer.raise_for_status()
            with open(datafile, 'w') as write_file:
                json.dump(answer.text, write_file)

            data = json.loads(answer.text)
            if datafile == FILE_FORECASTS:
                info_weather = data['data']
            else:
                info_airquality = data['data']

    except (OSError, Exception) as error:
        raise JSONRequestError(error)

    return info_weather, info_airquality


def loads_weather_data():
    """ :return: tuple(list, list) """

    info_weather = None
    info_airquality = None
    for datafile in (FILE_FORECASTS, FILE_AIRQUALITY):
        try:
            with open(datafile) as reader:
                data = json.loads(
                    json.load(reader)
                )
                if datafile is FILE_FORECASTS:
                    info_weather = data['data']
                else:
                    info_airquality = data['data']
        except (OSError, Exception) as error:
            raise JSONLoadsError(error)

    return info_weather, info_airquality


def preprocess(info):
    """
    0) determine position in time
    1) determine target times
    2) format time into keys
    3) determine time intervals

    Two process options based on time of day:
    I  MORNING -> EVENING
    II EVENING -> NIGHT

    :return: tuple(list, list)
    """
    current = datetime.datetime.now()
    now = datetime.datetime(
        current.year, current.month, current.day, current.hour, 00, 00
    )
    target = EVENING if current.time() < datetime.time(EVENING, 00, 00) else NIGHT
    target = datetime.datetime(
        current.year, current.month, current.day, target, 00, 00
    )
    tomorrow = current + datetime.timedelta(hours=24)
    tomorrow = datetime.datetime(
        tomorrow.year, tomorrow.month, tomorrow.day, TOMORROW, 00, 00
    )
    # weatherbit date example: '2021-06-22T06:00:00'
    key_time_now = str(now).replace(" ", "T")
    key_time_target = str(target).replace(" ", "T")
    key_time_tomorrow = str(tomorrow).replace(" ", "T")

    tomorrow_weather = None
    tomorrow_airquality = None
    interval_weather = None
    interval_airquality = None
    info_weather, info_airquality = info

    for data in (info_weather, info_airquality):
        now = 0
        target = 0
        tomorrow = 0
        for i, hour in enumerate(data):
            if hour['timestamp_local'] == key_time_now:
                now = i
            elif hour['timestamp_local'] == key_time_target:
                target = i
            elif hour['timestamp_local'] == key_time_tomorrow:
                tomorrow = i

        if data is info_weather:
            tomorrow_weather = data[tomorrow]
            interval_weather = data[now:target + 1]
        else:
            tomorrow_airquality = data[tomorrow]
            interval_airquality = data[now:target + 1]
    else:
        info_weather = interval_weather + [tomorrow_weather]
        info_airquality = interval_airquality + [tomorrow_airquality]

    # little paranoia
    if len(info_weather) < len(info_airquality):
        tail_wagon = len(info_airquality) - len(info_weather)
        info_weather += info_weather[0:tail_wagon]
    elif len(info_weather) > len(info_airquality):
        tail_wagon = len(info_weather) - len(info_airquality)
        info_airquality += info_airquality[0:tail_wagon]

    return info_weather, info_airquality


def format_weather(info):
    """
    Weather Forecast
        header
        hour1
        hour2
        ...
        tomorrow

    :return: forecast text
    """
    info_weather, info_airquality = info

    forecast_text = "Weather Forecast:"
    forecast_text += f"\n{'#TIME':<{W_TIME}} {'TMP':>{W_TEMP}}/{'FL':<{W_TEMP}}" \
                     f"  {'CLDS':>{W_CLD}}:{'PoP':<{W_CLD}}" \
                     f"  {'WIND <':>{W_WIND}} {'SPEED':^{W_SPEED}}  << {'GUST':>{W_GUST}}" \
                     f"  {'PRESSURE':^{W_AP}} {'UVI':^{W_UV + 2}} {'AIR QUALITY':^{W_AQI + 1}}"

    i = 0
    tomorrow = len(info_weather) - 1
    for weather, airquality in zip(info_weather, info_airquality):
        if i != tomorrow:
            ttime = f"\n*{weather['timestamp_local'][11:-3]}  "
        else:
            ttime = f"\ntomorrow"

        temp = f"{round(weather['temp'])}°"
        app_temp = f"{round(weather['app_temp'])}°"

        clouds = f"{round(weather['clouds']):03}%"
        precipitation = f"{round(weather['pop']):03}%"

        wind_direction = f"{weather['wind_cdir']} <"
        wind_speed = f"{deep_format(weather['wind_spd'], 'wind_speed')}m/s"
        wind_gust = f"{round(weather['wind_gust_spd'])}m/s"

        pressure = f"{deep_format(weather['pres'], 'pressure')}mmHg"
        ultraviolet = deep_format(weather['uv'], 'ultraviolet')
        air_quality_epa = deep_format(airquality['aqi'], 'aqi')

        forecast_text += f"{ttime:<{W_TIME}}= {temp:>{W_TEMP}}/{app_temp:<{W_TEMP}}" \
                         f"  {clouds:>{W_CLD}}:{precipitation:<{W_CLD}}" \
                         f"  {wind_direction:>{W_WIND}} {wind_speed:>{W_SPEED}}  << {wind_gust:>{W_GUST}}" \
                         f"  {pressure:>{W_AP}} {ultraviolet:>{W_UV}} {air_quality_epa:>{W_AQI}} "
        i += 1

    return forecast_text


def deep_format(value, key):
    """ :return: formatted str """

    category = dict
    if key == 'pressure':
        category = ATMOSPHERIC_PRESSURE
    elif key == 'wind_speed':
        category = BEAUFORT_SCALE
    elif key == 'ultraviolet':
        category = UV_INDEX
    elif key == 'aqi':
        category = AIR_QUALITY_EPA

    #  (low, high) is tuple in category dict
    if key == 'pressure':
        value = round(value / 1.333)  # mbar to mmHg
        low, high = category['normal']
        if value < low:
            value = f"low {value}"
        elif value > high:
            value = f"high {value}"
        else:
            value = f"norm {value}"
    else:
        value = round(value)
        for index in category:
            low, high = category[index]
            if low <= value <= high:
                value = f"{index} {value}"
                break

    return value


def check_alerts(output_text, info):
    """ check: temperature, precipitation, wind_speed, ultraviolet, air quality """
    
    info_weather, info_airquality = info
    alerts_massages = ""
    tomorrow = len(info_weather) - 1

    i = 0
    for weather, airquality in zip(info_weather, info_airquality):
        if i != tomorrow:
            ttime = f"\n~{weather['timestamp_local'][11:-3]}~~:"
        else:
            ttime = f"\ntomorrow:"
        alerts = ""

        temperature = weather['temp']
        if temperature <= ALERT_TEMPERATURE[0]:
            alerts += "`very cold`"
        elif temperature >= ALERT_TEMPERATURE[1]:
            alerts += "`very hot`"

        precipitation = weather['pop']
        if ALERT_PRECIPITATION[0] <= precipitation <= ALERT_PRECIPITATION[1]:
            alerts += "`precipitation is likely`"
        elif precipitation > ALERT_PRECIPITATION[1]:
            alerts += "`downfall`"

        wind_speed = weather['wind_spd']
        if ALERT_WIND_SPEED[0] <= wind_speed <= ALERT_WIND_SPEED[1]:
            alerts += "`strong gale`"
        elif wind_speed > ALERT_WIND_SPEED[1]:
            alerts += "`dangerous storm`"

        ultraviolet = weather['uv']
        if ALERT_ULTRAVIOLET[0] <= ultraviolet <= ALERT_ULTRAVIOLET[1]:
            alerts += "`high solar activity`"
        elif ultraviolet > ALERT_ULTRAVIOLET[1]:
            alerts += "`hazardous radiation`"

        air_quality = airquality['aqi']
        if ALERT_AIR_QUALITY[0] <= air_quality <= ALERT_AIR_QUALITY[1]:
            alerts += "`high pollution`"
        elif air_quality > ALERT_AIR_QUALITY[1]:
            alerts += "`big blowout of contamination`"

        if alerts:
            alerts_massages += ttime + alerts
        i += 1

    if alerts_massages:
        alerts_massages = "Alerts:" + alerts_massages
        output_text = alerts_massages + "\n\n" + output_text
    return output_text


def send_email(email_text):
    attempt = 0
    max_attempt = 3
    errors = []
    while True:
        connection = smtplib.SMTP(GMAIL_SMTP, GMAIL_SMTP_PORT)
        try:
            hello = connection.ehlo()
            assert hello[0] == 250, f"1 ehlo fail {hello[0]}"

            tls = connection.starttls()
            assert tls[0] == 220, f"2 starttls fail {tls[0]}"

            with open(GMAIL_ACCOUNT, 'br') as gmail:
                account = base64.b64decode(gmail.read()).decode('UTF-8')
                addressee = account
            with open(GMAIL_APP_PASSWORD, 'br') as app_password:
                password = base64.b64decode(app_password.read()).decode('UTF-8')

            authentication = connection.login(account, password)
            assert authentication[0] == 235, f"3 login fail {authentication[0]}"

            raw_text = email_text.encode('utf-8')
            result = connection.sendmail(account, addressee, raw_text)
            assert len(result) == 0, f"4 sendmail fail {result}"

        except (OSError, AssertionError, Exception) as error:
            errors.append(str(error))
            if attempt <= max_attempt:
                attempt += 1
                time.sleep(20)
            else:
                error_text = "SendMailError: " + "\n".join(errors)
                raise SendMailError(error_text)
        else:
            break
        finally:
            connection.quit()


if __name__ == "__main__":
    main()
