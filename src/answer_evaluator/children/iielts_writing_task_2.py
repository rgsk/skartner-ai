
import json

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from src.utils import read_file

ielts_writing_task_2_scoring_guide = read_file(
    'src/data/ielts_writing_task_2_scoring_guide.txt'
)
llm = ChatOpenAI()

chain = llm | StrOutputParser()


def ielts_writing_task_2_evaluate(task: str, attempt: str):
    prompt = f'''
        scoring_guide: {ielts_writing_task_2_scoring_guide}

        based on above infomation give a band and comment for below task attempt.
        task: {task}
        attempt: {attempt}

        your output should be in json only, eg. band:5,comment:"some string"
    '''

    result = chain.invoke(prompt)
    json_value = json.loads(result)
    return json_value
