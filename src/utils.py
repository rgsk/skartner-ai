# base64_img = encode_image(image_path)
import base64
import json
import os

import requests

from src import openai_client


def read_file(path):
    with open(path, 'r') as file:
        # Read the entire contents of the file
        file_contents = file.read()
        return file_contents


def get_as_base64(url):
    return base64.b64encode(requests.get(url).content).decode('utf-8')
