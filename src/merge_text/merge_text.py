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
        the first initial words which you have to take from first string,
        and the rest from the second string,
        only output the result of their merge, it should not be like "Final String: ....", just the final string.
    """
    return chain.invoke(message)
