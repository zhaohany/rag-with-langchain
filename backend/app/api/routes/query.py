from __future__ import annotations

from fastapi import APIRouter, status

from app.models.schemas import NotImplementedResponse, QueryRequest

router = APIRouter(tags=["query"])


@router.post(
    "/query",
    response_model=NotImplementedResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def query(_payload: QueryRequest) -> NotImplementedResponse:
    return NotImplementedResponse(
        status="not_implemented",
        message="Query API schema is ready. Implementation will be done in class.",
    )
