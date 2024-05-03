from typing import Any, List

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool, StructuredTool


class searchWord(BaseModel):
    """Search a word or to get meaning of a word or to run a prompt against a given word"""

    word: str = Field(description="the word we want to search")


class saveWord(BaseModel):
    """Save the word in the dictionary"""


class goToManagePrompts(BaseModel):
    """manage prompts or click manage prompts or go to manage prompts page"""


valid_prompt_description = """
the prompt we want to save, the prompt must contain word enclosed in curly brackets like {word}, this will act as a placeholder where we can pass the word when we are searching for meaning of a word,
eg. if user specified "list meaning of word and 3 examples", the prompt that you will pass to the function is "list meaning of word {word} and 3 examples" or "list meaning of {word} and 3 examples"
"""


class addNewPrompt(BaseModel):
    """start creating a new prompt or add new prompt, if user has specified the prompt then pass the prompt as an argument, otherwise empty string"""
    prompt: str = Field(description=valid_prompt_description)


class saveThePrompt(BaseModel):
    """save the prompt that user has provided"""
    prompt: str = Field(description=valid_prompt_description)


class typeWithKeyboard(BaseModel):
    """when user says type or type with keyboard"""
    value: str = Field(description="what user wanted to type")


how_to_locate_prompt_from_list = """
    Here's more details about prompt and how to locate it from a list of prompts
    note: that prompt has three fields id: str, text: str and default: bool,
    you will be given a list of prompts, your job is to return the id of prompt that user intends to edit
    user can ask you to edit in several ways for eg. 
    1. edit the first prompt, in this case you have to return the id of first prompt
    2. user can say edit the default prompt, in this case return the prompt id whose default is true
    3. user can mention a partial prompt and your job is to determine which prompts from the list matches most with the prompt mentioned by user and return id of that
"""


def func():
    pass


class editPromptInput(BaseModel):
    promptId: str = Field(description="the prompt id we want to edit")


editPrompt = StructuredTool.from_function(
    func=func,
    name="editPrompt",
    description=f"""start editing a prompt from a list of prompts,
    {how_to_locate_prompt_from_list}
    """,
    args_schema=editPromptInput
)


class selectPromptAsDefaultInput(BaseModel):
    promptId: str = Field(
        description="the prompt id we want to set as default")


selectPromptAsDefault = StructuredTool.from_function(
    func=func,
    name="selectPromptAsDefault",
    description=f"""select one of the prompts from a list of prompts as default,
    {how_to_locate_prompt_from_list}
    """,
    args_schema=selectPromptAsDefaultInput

)


tools: List[Any] = [searchWord, saveWord, goToManagePrompts, addNewPrompt,
                    saveThePrompt, typeWithKeyboard, editPrompt, selectPromptAsDefault]
