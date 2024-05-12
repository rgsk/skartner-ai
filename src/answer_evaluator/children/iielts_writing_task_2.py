
import json

from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from src.utils import read_file

ielts_writing_task_2_scoring_guide = read_file(
    'src/data/ielts_writing_task_2_scoring_guide.txt'
)


class Response(BaseModel):
    band: int = Field(
        description="numeric band for attempt based on scoring_guide")
    comment: str = Field(
        description="comment considering points in scoring_guide")


llm = ChatOpenAI()
structured_llm = llm.with_structured_output(Response, method="json_mode")
chain = structured_llm


def ielts_writing_task_2_evaluate(task: str, attempt: str):
    prompt = f'''
        you have to evaluate ielts writing task 2, based on following scoring_guide and task instructions.

        scoring_guide: <scoring_guide>{ielts_writing_task_2_scoring_guide}</scoring_guide>

        based on above infomation give a band and comment for below task attempt.
        task: <task>{task}</task>
        attempt: <attempt>{attempt}</attempt>

        respond in JSON with `band` and `comment` keys
        eg: band: 7, comment: "some string"
        
        make sure that band is an integer, and comment is a string
    '''
    result = chain.invoke(prompt)
    return result
