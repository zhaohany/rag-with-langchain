from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.schemas import QueryRequest, QueryResponse
from app.services.query_service import query_service

router = APIRouter(tags=["query"])


@router.post(
    "/query",
    response_model=QueryResponse,
)
def query(payload: QueryRequest) -> QueryResponse:
    try:
        result = query_service.run_query(payload.question)
    except (OSError, ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return QueryResponse.model_validate(result)
