import json

from langchain_aws import ChatBedrock
from langchain_core.output_parsers import StrOutputParser

from src.utils import read_file

llm = ChatBedrock(
    model_id="mistral.mistral-large-2402-v1:0",
    client=None
)
chain = llm | StrOutputParser()

gre_scoring_guide_analyze_an_issue_task = read_file(
    'src/data/gre_scoring_guide_analyze_an_issue_task.txt')
analyze_an_issue_sample_scoring = read_file(
    'src/data/analyze_an_issue_sample_scoring.txt')


def gre_analyze_an_issue_task(task: str, attempt: str):
    prompt = f'''
    scoring_guide: {gre_scoring_guide_analyze_an_issue_task}
    sample_scoring: {analyze_an_issue_sample_scoring}

    based on above infomation give a score and Reader Commentary for below task attempt.
    task: {task}
    attempt: {attempt}

    your output should be in json only, eg. score:1,reader_commentary:"some string"
'''
    result = chain.invoke(prompt)
    json_value = json.loads(result)
    return json_value
