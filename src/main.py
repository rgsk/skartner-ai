import base64

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

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
