#!/usr/bin/env python

import argparse
import os

import requests
from requests_oauthlib import OAuth1
from slacker import Slacker

CONDITIONS_CODES = {
    0: 'tornado',
    1: 'tropical storm',
    2: 'hurricane',
    3: 'severe thunderstorms',
    4: 'thunderstorms',
    5: 'mixed rain and snow',
    6: 'mixed rain and sleet',
    7: 'mixed snow and sleet',
    8: 'freezing drizzle',
    9: 'drizzle',
    10: 'freezing rain',
    11: 'showers',
    12: 'showers',
    13: 'snow flurries',
    14: 'light snow showers',
    15: 'blowing snow',
    16: 'snow',
    17: 'hail',
    18: 'sleet',
    19: 'dust',
    20: 'foggy',
    21: 'haze',
    22: 'smoky',
    23: 'blustery',
    24: 'windy',
    25: 'cold',
    26: 'cloudy',
    27: 'mostly cloudy (night)',
    28: 'mostly cloudy (day)',
    29: 'partly cloudy (night)',
    30: 'partly cloudy (day)',
    31: 'clear (night)',
    32: 'sunny',
    33: 'fair (night)',
    34: 'fair (day)',
    35: 'mixed rain and hail',
    36: 'hot',
    37: 'isolated thunderstorms',
    38: 'scattered thunderstorms',
    39: 'scattered thunderstorms',
    40: 'scattered showers',
    41: 'heavy snow',
    42: 'scattered snow showers',
    43: 'heavy snow',
    44: 'partly cloudy',
    45: 'thundershowers',
    46: 'snow showers',
    47: 'isolated thundershowers',
    3200: 'not available',
}

ACCEPTABLE_CONDITIONS = (13, 14, 16, 20, 21, 26, 27, 28, 29, 30, 31, 32, 33, 34, 41, 42, 43, 44, 46, 3200)


def get_current_conditions(location, client_key, client_secret):
    """
    Return the current weather conditions.
    """
    yahoo_api = 'https://weather-ydn-yql.media.yahoo.com/forecastrss'
    query_oauth = OAuth1(client_key, client_secret, signature_type='query')
    res = requests.get(yahoo_api, {'location': location, 'format': 'json'}, auth=query_oauth)
    data = res.json()

    rtn_val = ''
    if 'current_observation' in data and 'condition' in data['current_observation']:
        conditions = data['current_observation']['condition']
        wind = data['current_observation']['wind']
        rtn_val = {
            'temp': int(conditions['temperature']),
            'text': conditions['text'],
            'condition_code': int(conditions['code']),
            'wind_chill': int(wind['chill']),
        }

    return rtn_val


def get_message(location, client_key, client_secret):

    data = get_current_conditions(location, client_key, client_secret)
    if not data:
        exit('Yahoo returned no weather data.')

    temp = data['temp']
    wind_chill = data['wind_chill']
    weather_text = data['text'].lower()
    condition_code = data['condition_code']
    is_conditions_acceptable = condition_code in ACCEPTABLE_CONDITIONS

    if wind_chill < 35:
        walking_conditions = "It's freezing, maybe we should all skip the walk this time."
    elif 35 <= wind_chill <= 60 and is_conditions_acceptable is True:
        walking_conditions = "It's a little brisk for a walk, but doable."
    elif 60 < wind_chill <= 75 and is_conditions_acceptable is True:
        walking_conditions = "It's the perfect conditions for a walk."
    elif 75 < wind_chill <= 85 and is_conditions_acceptable is True:
        walking_conditions = "It's a little warm, but is still acceptable for some people."
    elif wind_chill > 85:
        walking_conditions = "Dang it's hot! Maybe we should all skip the walk this time."
    else:
        walking_conditions = f"Looks like the temperature is okay for a walk, but other conditions ({CONDITIONS_CODES.get(condition_code, 'unknown condition').title()}) make it seem a little iffy."

    return f"@channel {walking_conditions} It's currently {temp}°F (feels like {wind_chill}°F) and {weather_text}."


def get_env_var(var_name):
    rtn_val = os.environ.get(var_name)
    if rtn_val is None:
        exit(f'The environment variable {var_name} is required.')

    return rtn_val


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--dry-run', action='store_true', default=False, help='Test the output.')
    parser.add_argument('--channel', default='#walking', help='Slack channel.')
    parser.add_argument('--location', required=True, help='Location for weather (e.g. Manhattan,KS).')
    return parser.parse_args()


def command(args):
    message = get_message(
        location=args.location,
        client_key=get_env_var('YAHOO_CLIENT_KEY'),
        client_secret=get_env_var('YAHOO_CLIENT_SECRET'),
    )
    if args.dry_run is True:
        print(message)
    else:
        slack = Slacker(get_env_var('SLACK_API_TOKEN'))
        slack.chat.post_message(args.channel, message, as_user=True, parse='full')


if __name__ == '__main__':
    command(parse_args())
