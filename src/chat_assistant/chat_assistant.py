import concurrent.futures
import os
from typing import List

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_openai import ChatOpenAI

from src.aws_utils import get_presigned_url
from src.file_utils import read_text_file

load_dotenv()
# llm = ChatGroq(model="mixtral-8x7b-32768")
llm = ChatOpenAI(model="gpt-3.5-turbo")
# llm = ChatAnthropic(model="claude-3-sonnet-20240229")  # type: ignore

# prompt = ChatPromptTemplate.from_messages(
#     [
#         # ("system", "You are a helpful assistant. Try to keep your answers very short, consise and to the point."),
#         ("system", "You are a helpful assistant. Try to use context first to answer the question."),
#         MessagesPlaceholder(variable_name="context"),
#         MessagesPlaceholder(variable_name="history"),
#         ("human", "{question}"),
#     ]
# )

prompt = ChatPromptTemplate.from_template("""
Answer the following question, if the question is related to context or history provided use them:
<context>
{context}
</context>
<history>
{history}
</history>
Question: {question}""")


chain = prompt | llm | StrOutputParser()

MONGODB_URL = os.getenv('MONGODB_URL')
DATABASE_NAME = "langchain"
COLLECTION_NAME = "chat_histories"


chain_with_history = RunnableWithMessageHistory(
    chain,  # type: ignore
    lambda session_id:  MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=MONGODB_URL,  # type: ignore
        database_name=DATABASE_NAME,
        collection_name=COLLECTION_NAME,
    ),
    input_messages_key="question",
    history_messages_key="history",
)


def chat_assistant(session_id: str, user_message: str, files_attached_urls: List[str]):
    # Using ThreadPoolExecutor for parallel execution
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Get presigned URLs in parallel
        presigned_urls = executor.map(get_presigned_url, files_attached_urls)

        # Read text files from presigned URLs in parallel
        contents = executor.map(read_text_file, presigned_urls)
    context = []
    for content in contents:
        context.append(Document(page_content=content))
    return chain_with_history.invoke({"question": user_message, 'context': context}, config={"configurable": {"session_id": session_id}})


def get_chat_history_messages(session_id: str):

    assert MONGODB_URL is not None
    history = MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=MONGODB_URL,
        database_name=DATABASE_NAME,
        collection_name=COLLECTION_NAME,
    )
    return history.messages
