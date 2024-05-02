import base64

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.chat_assistant.chat_assistant import (chat_assistant,
                                               get_chat_history_messages)
from src.navigate_image.navigate_image import navigate_image
from src.navigate_skartner.navigate_skartner import navigate_skartner
from src.transcribe_handwritten_text import transcribe_handwritten_text

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
)


@app.get("/")
async def root():
    return {"message": "AI Server running on port final check 123: 9000"}


@app.post("/transcribe_handwritten_text")
async def transcribe(image: UploadFile = File(...)):
    image_bytes = await image.read()
    base64_img = base64.b64encode(image_bytes).decode('utf-8')
    content = transcribe_handwritten_text(base64_img)
    return {'content': content}


@app.get("/navigate_image")
async def navigate(user_query: str):
    content = navigate_image(user_query)
    return {'content': content}


@app.get("/navigate_skartner")
async def nav_sk(user_message: str):
    assistant_message = navigate_skartner(user_message)
    return {'assistant_message': assistant_message}


@app.get('/chat')
async def chat_endpoint(session_id: str, user_message: str):
    print(f'chat_assistant invoked {user_message=}')
    assistant_message = chat_assistant(session_id, user_message)
    print(f'chat_assistant outputted {assistant_message=}')
    return {'assistant_message': assistant_message}


@app.get('/chat_history')
async def chat_history_endpoint(session_id: str):
    messages = get_chat_history_messages(session_id)
    return {'messages': messages}
