# Function to encode the image as base64
import base64
import json
import os

from src.navigate_image.sample_form_image_positions import \
    sample_form_image_positions
from src.openai_client import openai_client
from src.skartner_server import get_jsondata_key, set_jsondata_key


def encode_image(image_path: str):
    # check if the image exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


image_path = 'src/navigate_image/form_image.png'
base64_img = encode_image(image_path)


def navigate_image(user_query: str):
    GPT_MODEL = "gpt-4-turbo-2024-04-09"
    # set_jsondata_key('formImagePositions', sample_form_image_positions)
    positions = get_jsondata_key('formImagePositions') or []
    # print(positions)
    response = openai_client.chat.completions.create(
        model=GPT_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"from the user query try to understand which button or text user wants to locate in the image, you have to return it's location, output in terms of top and left offset as a json object, for eg. for something in center output should be top:50%,left:50%, if you can't determine which button/text/icon user wants to locate, output top:-1%,left:-1%. refer these labels to get the idea for how to locate elements in this image - ${json.dumps(positions)}"
            },
            {
                "role": "user",
                "content": user_query
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}"
                        }
                    },
                ],
            },

        ],
    )
    content = response.choices[0].message.content
    if content is None:
        return None
    return json.loads(content)
