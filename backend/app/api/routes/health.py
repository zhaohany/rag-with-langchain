from __future__ import annotations

from fastapi import APIRouter

from app.models.schemas import HealthResponse
from app.services.health_service import health_service

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    payload = health_service.get_status()
    return HealthResponse.model_validate(payload)
