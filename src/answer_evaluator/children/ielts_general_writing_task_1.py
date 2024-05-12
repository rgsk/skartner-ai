

import json

from openai import OpenAI

from src.utils import read_file

ielts_writing_task_1_scoring_guide = read_file(
    'src/answer_evaluator/children/ielts_writing_task_1_scoring_guide.txt'
)

openai_client = OpenAI()
ielts_general_writing_task_1_sample_responses = read_file(
    'src/answer_evaluator/children/ielts_general_writing_task_1_sample_responses.txt'
)


def ielts_general_writing_task_1(task: str, attempt: str):
    GPT_MODEL = "gpt-3.5-turbo"
    # set_jsondata_key('formImagePositions', sample_form_image_positions)
    # print(positions)
    user_message = f'''
you have to evaluate ielts general writing task 1, based on following scoring_guide and sample_responses.

        scoring_guide: {ielts_writing_task_1_scoring_guide}
        sample_responses: {ielts_general_writing_task_1_sample_responses}

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
        ],
    )
    content = response.choices[0].message.content
    assert (isinstance(content, str))
    return json.loads(content)
