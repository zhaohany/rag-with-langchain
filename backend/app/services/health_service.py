from __future__ import annotations

import json

from app.core.config import settings


class HealthService:
    def get_status(self) -> dict[str, str | int | None]:
        ingestion_status = "idle"
        last_success_ingestion_time: str | None = None
        total_docs = 0

        if settings.system_meta_path.exists():
            try:
                raw = json.loads(settings.system_meta_path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    ingestion_status = str(raw.get("ingestion_status", "idle"))
                    last_value = raw.get("last_success_ingestion_time")
                    last_success_ingestion_time = str(last_value) if last_value else None
                    total_docs = int(raw.get("total_docs", 0))
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                ingestion_status = "idle"
                last_success_ingestion_time = None
                total_docs = 0

        return {
            "status": "ok",
            "version": settings.app_version,
            "environment": settings.env,
            "ingestion_status": ingestion_status,
            "last_success_ingestion_time": last_success_ingestion_time,
            "total_docs": total_docs,
        }


health_service = HealthService()
