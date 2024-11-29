from fastapi import APIRouter, HTTPException, Query

from app.models.models import ChatRequest
from app.repository.open_api import get_response_from_context, get_response_from_openai, get_context_from_query


router = APIRouter()


@router.post("/query")
async def handle_query(query_model: ChatRequest, from_context: bool = Query(False)):
    try:
        
        if from_context:
            # Use retrieval-based query
            answer = get_response_from_context(query_model.prompt)
        else:
            # Use direct OpenAI-based query
            answer = get_response_from_openai(query_model.prompt)

        return {"query": query_model.prompt, "answer": answer}
    except RuntimeError as e:
        # Handle errors in processing queries
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-context-from-query/")
async def handle_query(query_model: ChatRequest):
    try:
        answer = get_context_from_query(query_model.prompt)
        return {"query": query_model.prompt, "context": answer}
    except RuntimeError as e:
        # Handle errors in processing queries
        raise HTTPException(status_code=500, detail=str(e))