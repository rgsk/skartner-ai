

import json

from openai import OpenAI

from src.utils import get_as_base64, read_file

from .ielts_academic_writing_task_1_sample_responses import \
    ielts_academic_writing_task_1_sample_responses

ielts_writing_task_1_scoring_guide = read_file(
    'src/answer_evaluator/children/ielts_writing_task_1_scoring_guide.txt'
)

openai_client = OpenAI()


def ielts_academic_writing_task_1(task: str, image_url: str, attempt: str):
    base64_img = get_as_base64(image_url)
    GPT_MODEL = "gpt-4-turbo-2024-04-09"
    # set_jsondata_key('formImagePositions', sample_form_image_positions)
    # print(positions)
    user_message = f'''
    you have to evaluate ielts academic writing task 1, based on following scoring_guide and sample responses.
    the task is accompanied by an image, if image is not related to task, then give a band of -1.
    implying that image and task are different.

            scoring_guide: {ielts_writing_task_1_scoring_guide}
            sample_responses: {ielts_academic_writing_task_1_sample_responses}

            based on above infomation give a band and comment for below task attempt.
            task: {task}
            attempt: {attempt}
            
            respond in JSON with `band` and `comment` keys
            eg: band: 7, comment: "some string"
            
            make sure that band is an integer, and comment is a string

    '''
    # print(user_message)
    response = openai_client.chat.completions.create(
        model=GPT_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": user_message
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_img}"
                        }
                    },
                ],
            },

        ],
    )
    content = response.choices[0].message.content
    assert (isinstance(content, str))
    return json.loads(content)
