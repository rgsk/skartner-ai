from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "AI Server running on port changed: 9000"}
