from typing import Any

from langchain_anthropic import ChatAnthropic

from src.navigate_skartner.tools import tools

llm = ChatAnthropic(model="claude-3-sonnet-20240229")  # type: ignore

llm_with_tools = llm.bind_tools(tools)


def navigate_skartner(user_message: str):
    result: Any = llm_with_tools.invoke(user_message)
    return result
