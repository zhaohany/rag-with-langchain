# Homework: Ingest Background Job

## Goal

`POST /api/v1/ingest` now works as an async background job. The API returns `{"status":"queued"}` immediately, and FastAPI `BackgroundTasks` runs the ingestion pipeline in the background.

You need to complete two TODOs to make the full flow work.

## Background

The following components are already implemented:

- `IngestQueueService.submit_ingest_job()` — creates a job record in SQLite, updates status, and schedules the background task.
- `DatabaseStore.mark_ingest_job_running()` — marks a job as `running`.
- `DatabaseStore.mark_ingest_job_succeeded()` — marks a job as `succeeded`.
- `DatabaseStore.mark_ingest_job_failed()` — marks a job as `failed`.
- `IngestService.run_sync_ingest()` — the existing sync pipeline (discover, chunk, embed, persist).

Two parts are left as exercises:

### Task 1: `DatabaseStore.create_ingest_job` — Fill in the SQL column list

**File:** `backend/app/services/database_store.py`

**What to do:**

The SQL INSERT statement has an empty column list. Fill it in so the statement inserts one row into `ingest_jobs`.

The table `ingest_jobs` has these columns:

| Column | Type | Example |
|---|---|---|
| `job_id` | TEXT | `"ingest_20260628_123456_000000"` |
| `status` | TEXT | `"queued"` |
| `message` | TEXT | `"Ingestion job submitted"` |
| `created_at` | TEXT | ISO 8601 UTC timestamp |
| `started_at` | TEXT | NULL (set later) |
| `finished_at` | TEXT | NULL (set later) |

The current code:

```python
sql = """
INSERT INTO ingest_jobs (
    -- TODO(sql): fill in the column list.
    -- Expected columns:
    -- job_id, status, message, created_at, started_at, finished_at
)
VALUES (?, 'queued', ?, ?, NULL, NULL)
"""
conn.execute(sql, (job_id, message, utc_now_iso()))
```

The `VALUES` clause already has 5 placeholders: `(?, 'queued', ?, ?, NULL, NULL)`.

Your column list must match the values:
1. `job_id` — from `?` (first param)
2. `status` — hardcoded `'queued'`
3. `message` — from `?` (second param)
4. `created_at` — from `?` (third param)
5. `started_at` — hardcoded `NULL`
6. `finished_at` — hardcoded `NULL`

**Hint:**

The completed SQL should look like:

```sql
INSERT INTO ingest_jobs (
    job_id, status, message, created_at, started_at, finished_at
)
VALUES (?, 'queued', ?, ?, NULL, NULL)
```

Remove the `-- TODO(sql)` comment lines after you fill them in.

---

### Task 2: `IngestQueueService.process_ingest_job` — Call `run_sync_ingest()`

**File:** `backend/app/services/ingest_queue_service.py`

**What to do:**

The function `process_ingest_job` currently raises `NotImplementedError`. Replace that line with the actual call to the existing sync ingest pipeline.

The current code:

```python
def process_ingest_job(self, job_id: str) -> None:
    self.database.mark_ingest_job_running(job_id)

    try:
        # TODO: call existing sync ingest pipeline and build success message.
        # Hint: use self.ingest_service.run_sync_ingest().
        raise NotImplementedError(
            "Call self.ingest_service.run_sync_ingest() and build message."
        )
        self.database.mark_ingest_job_succeeded(job_id, message)
    except RuntimeError as exc:
        self.database.mark_ingest_job_failed(job_id, str(exc))
    except Exception as exc:
        ...
```

Replace the `raise NotImplementedError(...)` line with:

```python
result = self.ingest_service.run_sync_ingest()
message = (
    "Ingestion completed: "
    f"docs={result['total_docs']}, chunks={result['total_chunks']}"
)
```

`run_sync_ingest()` returns a dict with keys `total_docs` and `total_chunks`. Use those to build `message`. The `mark_ingest_job_succeeded` call after it will persist this message.

Remove the `# TODO` comment line after you finish.

---

## How to Test

Start the backend:

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Submit an ingest job:

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool
```

Expected response:

```json
{
  "status": "queued",
  "total_docs": 0,
  "total_chunks": 0,
  "message": "Ingestion job submitted",
  "job_id": "ingest_20260628_123456_000000"
}
```

Check health to see status transition:

```bash
curl -s http://127.0.0.1:8000/api/v1/health | python3 -m json.tool
```

Expected: `ingestion_status` should change from `"queued"` → `"running"` → `"idle"` after the background job completes.

Try a second submit while one is running:

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool
```

Expected: `HTTP 409` with detail `"Ingestion is already queued/running. Please wait."`

## Inspect the SQLite table

```bash
sqlite3 data/meta/rag.sqlite3
```

Inside the shell:

```sql
SELECT * FROM ingest_jobs;
.quit
```

You should see one row with status transitions.

## Success Criteria

- `POST /api/v1/ingest` returns `{"status":"queued", ...}` instead of running synchronously.
- `GET /api/v1/health` eventually shows `"ingestion_status":"idle"` with updated `total_docs`.
- A second `/ingest` call while one is running returns `409 Conflict`.
- The `ingest_jobs` table in SQLite has a row documenting the job lifecycle.
