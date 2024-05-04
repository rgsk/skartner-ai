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


def gre_analyze_an_issue_task_evaluate(task: str, attempt: str):
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


def gre_analyze_an_issue_task_generate(task: str, score: int):
    prompt = f'''
    scoring_guide: {gre_scoring_guide_analyze_an_issue_task}
    sample_scoring: {analyze_an_issue_sample_scoring}

    based on above infomation provide solution to above task that would have score of {score},
    only provide the solution and nothing else.
    Make sure you follow the scoring guide and sample responses,
    ensure that the solution you generate has the writing skill-level similar to responses corresponding to that score in sample_scoring.
    This implies you have incorporate grammatical/spelling mistakes appropriately for lower scores.
    task: {task}
'''
    result = chain.invoke(prompt)
    return {'solution': result}
