from fastapi import  APIRouter
from app.routes.apis.v1 import  open_api

api_router = APIRouter()
api_router.include_router(open_api.router, prefix="/openai", tags=["openai"])