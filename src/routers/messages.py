import json
import os
from typing import List, Optional, Union

import motor.motor_asyncio
from fastapi import APIRouter
from pydantic import BaseModel, BeforeValidator, Field
from typing_extensions import Annotated

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.langchain
messages_collection = db.get_collection("chat_histories")

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class MessageModel(BaseModel):
    """
    Container for a single message record.
    """

    # The primary key for the MessageModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    SessionId: str
    History: Union[dict, str]

    @classmethod
    def model_validate(cls, obj):
        obj['History'] = json.loads(obj['History']) if isinstance(
            obj['History'], str) else obj['History']
        return super().model_validate(obj)


class MessageCollection(BaseModel):
    """
    A container holding a list of `MessageModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    messages: List[MessageModel]


@router.get(
    "/",
    response_description="List all messages",
    response_model=MessageCollection,
    response_model_by_alias=False,
)
async def list_messages():
    """
    List all of the message data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    messages = await messages_collection.find().to_list(1000)
    parsed_messages = [MessageModel.model_validate(msg) for msg in messages]
    return MessageCollection(messages=parsed_messages)


@router.get(
    "/sessions",
    response_description="List sessions with by prefix",
    response_model=List[str],
    response_model_by_alias=False,
)
async def list_sessions(prefix: str):
    """
    List sessions with by prefix
    """
    query = {}  # Initialize an empty query
    if prefix:
        # If prefix is provided, construct a query to filter by SessionId
        # Filter by SessionId starting with the prefix
        query['SessionId'] = {"$regex": f"^{prefix}"}

    unique_session_ids = await messages_collection.distinct("SessionId", query)
    return unique_session_ids
