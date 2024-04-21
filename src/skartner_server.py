import json
import os
from typing import Any

import requests

SKARTNER_SERVER = os.getenv('SKARTNER_SERVER')


def get_jsondata_key(key: str):
    url = f'{SKARTNER_SERVER}/jsonData/{key}'
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if json_data:
            return json_data['value']


def set_jsondata_key(key: str, value: Any):
    url = f'{SKARTNER_SERVER}/jsonData/{key}'
    response = requests.post(url, data=json.dumps(value), headers={
        "Content-Type": "application/json"
    })
    if response.status_code == 200:
        json_data = response.json()
        if json_data:
            return json_data['value']
