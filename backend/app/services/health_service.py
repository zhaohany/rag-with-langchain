from __future__ import annotations

from typing import Union

from app.core.config import settings
from app.services.database_store import database_store


class HealthService:
    def get_status(self) -> dict[str, Union[str, int, None]]:
        meta = database_store.get_system_meta()

        return {
            "status": "ok",
            "version": settings.app_version,
            "environment": settings.env,
            "ingestion_status": str(meta.get("ingestion_status") or "idle"),
            "last_success_ingestion_time": str(meta["last_success_ingestion_time"]) if meta.get("last_success_ingestion_time") else None,
            "total_docs": int(meta.get("total_docs") or 0),
        }


health_service = HealthService()
