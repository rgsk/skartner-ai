from enum import Enum
from typing import Any, List

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool


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


class goToWordOrSearchTab(BaseModel):
    """when user says go to word tab or search tab"""


class goToDictionaryOrHistoryTab(BaseModel):
    """when user says go to dictionary tab or history tab"""


class deleteWord(BaseModel):
    """delete the word"""


class swipeLeft(BaseModel):
    """swipe left or go to next page or go to next word or go right"""


class swipeRight(BaseModel):
    """swipe right or go to previous page or go to previous word or go left"""


class clearFilters(BaseModel):
    """clear all the filters or reset filters"""


class goToStatusPage(BaseModel):
    """go to status page or change status filters"""


class goToTagsPage(BaseModel):
    """go to tags page or change tags filters"""


class goBack(BaseModel):
    """go back or click back or go to previous page"""


class goToPage(BaseModel):
    """switch to a certain page number or switch to word number _, because one word is displayed per page"""
    page: int = Field(description="the page number that user wants to go to")


class goToFirstPage(BaseModel):
    """go to first page or go to first word"""


class goToLastPage(BaseModel):
    """go to last page or go to last word"""


class filterByWordOrCharacters(BaseModel):
    """user could say like filter for the words starting with s t, in this case 'st' would be filter_value,
    """
    filter_value: str = Field(
        description="the word or a sequence of few characters")


class StatusEnum(str, Enum):
    ALMOST_LEARNT = "ALMOST_LEARNT"
    FINISHED_LEARNING = "FINISHED_LEARNING"
    MASTERED = "MASTERED"
    MEMORY_MODE = "MEMORY_MODE"
    STARTED_LEARNING = "STARTED_LEARNING"
    STILL_LEARNING = "STILL_LEARNING"


class setStatus(BaseModel):
    """Update/set/change status to a new value"""
    value: StatusEnum = Field(..., description="The new status to be set")


class TagType(str, Enum):
    page = "page"
    word = "word"
    all = "all"


tag_type_description = "if it is specifically mentioned that do this action for page or word, then tag_type should be that value, otherwise all"


class addTag(BaseModel):
    """add tag or select tag"""
    tag_name: str = Field(
        description="the tag name to add or select")
    tag_type: TagType = Field(
        description=tag_type_description)


class removeTag(BaseModel):
    """remove tag or unselect tag"""
    tag_name: str = Field(
        description="the tag name to remove or unselect")
    tag_type: TagType = Field(
        description=tag_type_description)


tools: List[Any] = [
    searchWord, saveWord, goToManagePrompts, addNewPrompt, saveThePrompt, typeWithKeyboard, editPrompt,
    selectPromptAsDefault, goToWordOrSearchTab, goToDictionaryOrHistoryTab, deleteWord, swipeLeft,
    swipeRight, clearFilters, goToStatusPage, goToTagsPage, goBack, goToPage, goToFirstPage, goToLastPage,
    filterByWordOrCharacters, setStatus, addTag, removeTag
]
