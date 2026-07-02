# Ingest Background Job

## Overview

`POST /api/v1/ingest` now uses an async background job pattern. Instead of running embedding synchronously, the API schedules the ingestion pipeline via FastAPI `BackgroundTasks` and returns immediately.

## Sequence

```
Client                     FastAPI                         SQLite
  |                          |                               |
  |  POST /api/v1/ingest     |                               |
  |------------------------->|                               |
  |                          |  CREATE ingest_jobs (queued)  |
  |                          |------------------------------>|
  |                          |  UPDATE system_meta (queued)  |
  |                          |------------------------------>|
  |  202 {"status":"queued"} |                               |
  |<-------------------------|                               |
  |                          |                               |
  |                          |  [BackgroundTasks runs]       |
  |                          |  mark_ingest_job_running()    |
  |                          |------------------------------>|
  |                          |  run_sync_ingest()            |
  |                          |  mark_ingest_job_succeeded()  |
  |                          |------------------------------>|
```

## Key Design Decisions

- Uses FastAPI built-in `BackgroundTasks` (not Celery / Redis queue).
- One `/ingest` request = one job that rebuilds the full local index.
- Returns `409 Conflict` if a job is already `queued` or `running`.
- Job status is persisted in the SQLite `ingest_jobs` table.

## Files Changed

| File | Change |
|---|---|
| `app/api/routes/ingest.py` | Switch to `BackgroundTasks` + `IngestQueueService` |
| `app/services/ingest_queue_service.py` | New: queue orchestration layer |
| `app/services/database_store.py` | Add `ingest_jobs` table and CRUD methods |
| `app/models/schemas.py` | `IngestResponse` gains `job_id` field |

## Student Homework

See `docs/homework-ingest-background-job.md` for detailed assignment instructions.
