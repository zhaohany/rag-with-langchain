from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Union

from app.core.config import settings


DEFAULT_SYSTEM_META: dict[str, Union[str, int, None]] = {
    "ingestion_status": "idle",
    "last_success_ingestion_time": None,
    "total_docs": 0,
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class DatabaseStore:
    def __init__(self, database_path: Optional[Path] = None) -> None:
        self._database_path = database_path

    @property
    def database_path(self) -> Path:
        return self._database_path or settings.database_path

    def get_system_meta(self) -> dict[str, Union[str, int, None]]:
        """Read ingest status from SQLite with safe fallback."""
        try:
            with self._connect() as conn:
                row = conn.execute(
                    """
                    SELECT ingestion_status, last_success_ingestion_time, total_docs
                    FROM system_meta
                    WHERE id = ?
                    """,
                    (1,),
                ).fetchone()
        except (OSError, sqlite3.DatabaseError, ValueError, TypeError):
            return dict(DEFAULT_SYSTEM_META)

        if row is None:
            return dict(DEFAULT_SYSTEM_META)

        return {
            "ingestion_status": str(row["ingestion_status"] or "idle"),
            "last_success_ingestion_time": str(row["last_success_ingestion_time"]) if row["last_success_ingestion_time"] else None,
            "total_docs": int(row["total_docs"] or 0),
        }

    def write_system_meta(self, payload: dict[str, Union[str, int, None]]) -> None:
        """Homework: upsert ingest status into SQLite.

        Students should implement this function.

        Setup already provided:
        - `self._connect()` opens the SQLite database.
        - `_init_schema(...)` creates the required tables.
        - `current` and `next_payload` are already prepared below.
        - Students only need to replace the TODO with the INSERT/UPDATE SQL logic.

        Input:
        - `payload`: partial or full system metadata.

        Example input:
        ```python
        {
            "ingestion_status": "idle",
            "last_success_ingestion_time": "2026-06-04T12:00:00Z",
            "total_docs": 3,
        }
        ```

        Output:
        - Return `None`.
        - Persist exactly one row in the `system_meta` table with `id = 1`.

        Required behavior:
        - Merge `payload` with the current metadata from `self.get_system_meta()` so partial updates keep existing fields.
        - Insert the row if it does not exist.
        - Update the row if it already exists.

        Syntax hints:
        - Dict merge syntax works in Python 3.9: `next_payload = {**current, **payload}`.
        - Use parameterized SQL placeholders: `VALUES (1, ?, ?, ?)`.
        - SQLite upsert syntax is `ON CONFLICT(id) DO UPDATE SET column = excluded.column`.
        - Use `with self._connect() as conn:` and `conn.execute(sql, params)`.

        SQL shape example:
        ```python
        conn.execute(
            "INSERT INTO ... VALUES (...) ON CONFLICT(id) DO UPDATE SET ...",
            (...),
        )
        ```
        """
        current = self.get_system_meta()
        next_payload = {**current, **payload}

        with self._connect() as conn:
            raise NotImplementedError("Homework: write INSERT/UPDATE SQL for system_meta")

    def replace_chunk_metadata(self, records: list[dict[str, Any]]) -> None:
        """Homework: replace all chunk metadata in SQLite after ingest.

        Students should implement this function.

        Setup already provided:
        - `self._connect()` opens the SQLite database.
        - `_init_schema(...)` creates the required tables.
        - `rows` is already prepared below.
        - Students only need to replace the TODO with DELETE + batch INSERT SQL logic.

        Input:
        - `records`: list of chunk dictionaries produced by `IngestService._step_chunk`.

        Example input:
        ```python
        [
            {
                "doc_id": "doc_1",
                "chunk_id": "doc_1_chunk_1",
                "source": "company_it_support_playbook.md",
                "chunk_index": 1,
                "chunk_text": "# IT Support ...",
            }
        ]
        ```

        Output:
        - Return `None`.
        - Delete old rows from `chunks`.
        - Insert one row per input record.

        Required behavior:
        - Keep the operation inside one database connection so delete + insert happen together.
        - Store columns in this order: `chunk_id`, `doc_id`, `source`, `chunk_index`, `chunk_text`.
        - Cast values before inserting to keep database rows predictable.

        Syntax hints:
        - A list comprehension can convert dicts to tuples for `executemany`.
        - Use `conn.execute("DELETE FROM chunks")` before inserting new rows.
        - Use `conn.executemany("INSERT INTO chunks (...) VALUES (?, ?, ?, ?, ?)", rows)` for batch insert.

        SQL shape example:
        ```python
        conn.execute("DELETE FROM chunks")
        conn.executemany("INSERT INTO chunks (...) VALUES (?, ?, ?, ?, ?)", rows)
        ```
        """
        rows = [
            (
                str(record["chunk_id"]),
                str(record["doc_id"]),
                str(record["source"]),
                int(record["chunk_index"]),
                str(record["chunk_text"]),
            )
            for record in records
        ]

        with self._connect() as conn:
            raise NotImplementedError("Homework: write DELETE + batch INSERT SQL for chunks")

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        self._init_schema(conn)
        return conn

    def _init_schema(self, conn: sqlite3.Connection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS system_meta (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                ingestion_status TEXT NOT NULL,
                last_success_ingestion_time TEXT,
                total_docs INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                doc_id TEXT NOT NULL,
                source TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                chunk_text TEXT NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON chunks (doc_id)")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ingest_jobs (
                job_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                message TEXT,
                created_at TEXT NOT NULL,
                started_at TEXT,
                finished_at TEXT
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_ingest_jobs_status ON ingest_jobs (status)"
        )

    def create_ingest_job(self, job_id: str, message: str) -> None:
        """Create one queued ingestion job record.

        中文说明：
        在 /ingest API 接收到请求后，先写入一条 job record。
        这条记录表示任务已经进入 queued 状态，后台任务稍后会继续处理。

        English keywords:
        SQL INSERT, job record, queued status, timestamp

        Input:
        job_id: ingestion job id, e.g. "ingest_20260628_123456_000000"
        message: readable job message, e.g. "Ingestion job submitted"

        Output:
        None. The job row is written to SQLite table `ingest_jobs`.

        TODO(sql):
        Fill in the SQL statement below. It should insert one row into
        `ingest_jobs` with:
        - job_id from input
        - status = "queued"
        - message from input
        - created_at = current UTC timestamp
        - started_at = NULL
        - finished_at = NULL
        """
        with self._connect() as conn:
            sql = """
            INSERT INTO ingest_jobs (
                -- TODO(sql): fill in the column list.
                -- Expected columns:
                -- job_id, status, message, created_at, started_at, finished_at
            )
            VALUES (?, 'queued', ?, ?, NULL, NULL)
            """
            conn.execute(
                sql,
                (job_id, message, utc_now_iso()),
            )

    def mark_ingest_job_running(self, job_id: str) -> None:
        """Mark an ingestion job as running."""
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE ingest_jobs
                SET status = 'running',
                    message = 'Ingestion job is running',
                    started_at = ?
                WHERE job_id = ?
                """,
                (utc_now_iso(), job_id),
            )

    def mark_ingest_job_succeeded(self, job_id: str, message: str) -> None:
        """Mark an ingestion job as succeeded."""
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE ingest_jobs
                SET status = 'succeeded',
                    message = ?,
                    finished_at = ?
                WHERE job_id = ?
                """,
                (message, utc_now_iso(), job_id),
            )

    def mark_ingest_job_failed(self, job_id: str, message: str) -> None:
        """Mark an ingestion job as failed."""
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE ingest_jobs
                SET status = 'failed',
                    message = ?,
                    finished_at = ?
                WHERE job_id = ?
                """,
                (message, utc_now_iso(), job_id),
            )


database_store = DatabaseStore()
