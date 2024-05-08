from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

chain = llm | StrOutputParser()


def merge_text(first: str, second: str):
    message = f"""
        you are given two strings.
        first_string: {first}
        second_string: {second}

        your job is to merge them into single string,
        the first sentence of first_string is more correct and complete,
        for rest of the output second_string is better,
        only output the result of their merge, it should not be like "Final String: ....", just the final string.
    """
    return chain.invoke(message)
