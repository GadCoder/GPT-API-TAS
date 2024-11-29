from fastapi import FastAPI
from app.routes.base import api_router
app = FastAPI(title="Chatbot Backend", version="1.0")

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Chatbot Backend is running!"}
