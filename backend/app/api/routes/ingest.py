from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.schemas import IngestResponse
from app.services.ingest_service import ingest_service

router = APIRouter(tags=["ingest"])


@router.post(
    "/ingest",
    response_model=IngestResponse,
)
def ingest() -> IngestResponse:
    try:
        payload = ingest_service.run_sync_ingest()
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return IngestResponse.model_validate(payload)
