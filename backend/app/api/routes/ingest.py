from __future__ import annotations

from fastapi import APIRouter, status

from app.models.schemas import IngestRequest, NotImplementedResponse

router = APIRouter(tags=["ingest"])


@router.post(
    "/ingest",
    response_model=NotImplementedResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def ingest(_payload: IngestRequest) -> NotImplementedResponse:
    return NotImplementedResponse(
        status="not_implemented",
        message="Ingest API schema is ready. Implementation will be done in class.",
    )
