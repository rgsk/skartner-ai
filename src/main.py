import base64
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.answer_evaluator.children.ielts_academic_writing_task_1 import \
    ielts_academic_writing_task_1
from src.answer_evaluator.children.ielts_general_writing_task_1 import \
    ielts_general_writing_task_1
from src.answer_evaluator.children.iielts_writing_task_2 import \
    ielts_writing_task_2_evaluate
from src.merge_text.merge_text import merge_text

from .answer_evaluator.children.gre_analyze_an_issue_task import (
    gre_analyze_an_issue_task_evaluate, gre_analyze_an_issue_task_generate)
from .chat_assistant.chat_assistant import (chat_assistant,
                                            get_chat_history_messages)
from .crud.students import router as students_router
from .navigate_image.navigate_image import navigate_image
from .navigate_skartner.navigate_skartner import navigate_skartner
from .routers.messages import router as messages_router
from .transcribe_handwritten_text import transcribe_handwritten_text

load_dotenv()

app = FastAPI(
    title="Student Course API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)

app.include_router(students_router)
app.include_router(messages_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


class ChatRequestBody(BaseModel):
    session_id: str
    user_message: str
    files_attached_urls: List[str]


@app.post('/chat')
async def chat_endpoint_post(body: ChatRequestBody):
    user_message = body.user_message
    session_id = body.session_id
    files_attached_urls = body.files_attached_urls
    print(f'chat_assistant invoked {user_message=}')
    assistant_message = chat_assistant(
        session_id, user_message, files_attached_urls)
    print(f'chat_assistant outputted {assistant_message=}')
    return {'assistant_message': assistant_message}


@app.get('/chat_history')
async def chat_history_endpoint(session_id: str):
    messages = get_chat_history_messages(session_id)
    return {'messages': messages}


class TaskRequest(BaseModel):
    type: str
    args: dict


@app.post("/answer_evaluator")
async def answer_evaluator(task_request: TaskRequest):
    if task_request.type == 'gre_analyze_an_issue_task':
        task = task_request.args.get('task')
        attempt = task_request.args.get('attempt')
        if task is None or attempt is None or task == '' or attempt == '':
            raise HTTPException(
                status_code=400, detail="tasks and attempt should be non-empty")
        return gre_analyze_an_issue_task_evaluate(task, attempt)
    elif task_request.type == 'ielts_writing_task_2':
        task = task_request.args.get('task')
        attempt = task_request.args.get('attempt')
        if task is None or attempt is None or task == '' or attempt == '':
            raise HTTPException(
                status_code=400, detail="tasks and attempt should be non-empty")
        return ielts_writing_task_2_evaluate(task, attempt)
    elif task_request.type == 'ielts_academic_writing_task_1':
        task = task_request.args.get('task')
        image_url = task_request.args.get('image_url')
        attempt = task_request.args.get('attempt')
        if task is None or image_url is None or attempt is None or task == '' or image_url == '' or attempt == '':
            raise HTTPException(
                status_code=400, detail="tasks, image_url and attempt should be non-empty")
        return ielts_academic_writing_task_1(task, image_url, attempt)
    elif task_request.type == 'ielts_general_writing_task_1':
        task = task_request.args.get('task')
        attempt = task_request.args.get('attempt')
        if task is None or attempt is None or task == '' or attempt == '':
            raise HTTPException(
                status_code=400, detail="tasks and attempt should be non-empty")
        return ielts_general_writing_task_1(task, attempt)
    else:
        raise HTTPException(status_code=400, detail="Invalid task type")


@app.post("/answer_generator")
async def answer_generator(task_request: TaskRequest):
    if task_request.type == 'gre_analyze_an_issue_task':
        task = task_request.args.get('task')
        score = task_request.args.get('score')
        if task is None or score is None or task == '':
            raise HTTPException(
                status_code=400, detail="tasks and score should be non-empty")
        return gre_analyze_an_issue_task_generate(task, score)
    else:
        raise HTTPException(status_code=400, detail="Invalid task type")


class MergeTextRequest(BaseModel):
    first: str
    second: str


@app.post('/merge_text')
async def merge_text_endpoint(req: MergeTextRequest):
    return merge_text(req.first, req.second)
#
