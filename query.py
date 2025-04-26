from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from llm_service import get_llm_response

router = APIRouter(prefix="/api", tags=["query"])

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    response: dict
    original_question: str

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        response = await get_llm_response(request.question)
        return QueryResponse(response=response, original_question=request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))