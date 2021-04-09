import requests

from rent.utilities.utilities import get_line_token, get_line_token_of_yu

URL = 'https://notify-api.line.me/api/notify'


def send_message(msg):
    headers = {'Authorization': 'Bearer ' + get_line_token()}
    payload = {'message': msg}
    r = requests.post(URL, headers=headers, params=payload)
    return r.status_code

def send_message_to_yu(msg):
    headers = {'Authorization': 'Bearer ' + get_line_token_of_yu()}
    payload = {'message': msg}
    r = requests.post(URL, headers=headers, params=payload)
    return r.status_code
