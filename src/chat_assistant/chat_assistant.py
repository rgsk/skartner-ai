import os

from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

load_dotenv()
llm = ChatBedrock(
    model_id="mistral.mistral-large-2402-v1:0",
    client=None,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Try to keep your answers very short, consise and to the point."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

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


def chat_assistant(session_id: str, user_message: str):
    return chain_with_history.invoke({"question": user_message}, config={"configurable": {"session_id": session_id}})


def get_chat_history_messages(session_id: str):

    assert MONGODB_URL is not None
    history = MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=MONGODB_URL,
        database_name=DATABASE_NAME,
        collection_name=COLLECTION_NAME,
    )
    return history.messages
