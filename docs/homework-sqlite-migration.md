# Homework: SQLite Metadata Migration

## Goal

In this homework, you will complete a small database migration inside the backend.

The project used to store metadata in local JSON files. The backend now uses a local SQLite database file instead:

```text
data/meta/rag.sqlite3
```

Your task is to finish the SQL write logic in `DatabaseStore`.

## What Is SQLite?

SQLite is a lightweight relational database.

Unlike PostgreSQL or MySQL, SQLite does not require a separate database server. It stores data in a normal local file, such as:

```text
data/meta/rag.sqlite3
```

This makes SQLite useful for local development, demos, small services, and embedded applications.

In this project:

- FAISS still stores the vector index files in `data/index/`.
- SQLite stores structured metadata such as ingest status and chunk metadata.
- The backend talks to SQLite through Python's built-in `sqlite3` module.

## Why Migrate From JSON To SQLite?

JSON files are simple, but they become harder to manage when the app grows.

SQLite gives us:

- Structured tables and columns
- Safer updates than manually rewriting JSON files
- Better support for querying by fields
- Better concurrency behavior, especially with WAL mode
- A clean path toward future database-backed features

## Files To Read

Start with this file:

```text
backend/app/services/database_store.py
```

You should also understand how it is used by:

```text
backend/app/services/ingest_service.py
backend/app/services/health_service.py
```

## What Is Already Provided

The database connection and schema setup are already implemented for you.

You do not need to create the database connection from scratch.

You do not need to create the tables from scratch.

The provided method below opens the SQLite database and initializes the schema:

```python
def _connect(self) -> sqlite3.Connection:
    self.database_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(self.database_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    self._init_schema(conn)
    return conn
```

The provided schema includes two tables:

```sql
CREATE TABLE IF NOT EXISTS system_meta (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    ingestion_status TEXT NOT NULL,
    last_success_ingestion_time TEXT,
    total_docs INTEGER NOT NULL DEFAULT 0
)
```

```sql
CREATE TABLE IF NOT EXISTS chunks (
    chunk_id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    source TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL
)
```

## Example Function Already Implemented

`get_system_meta` is already implemented. Treat it as your reference example.

It demonstrates:

- Opening a database connection with `with self._connect() as conn:`
- Running a SQL query with `conn.execute(...)`
- Using parameterized SQL with `?`
- Reading one row with `.fetchone()`
- Returning safe default values when the database is empty or invalid

Example pattern:

```python
with self._connect() as conn:
    row = conn.execute(
        """
        SELECT ingestion_status, last_success_ingestion_time, total_docs
        FROM system_meta
        WHERE id = ?
        """,
        (1,),
    ).fetchone()
```

## Your Tasks

You need to complete two functions in:

```text
backend/app/services/database_store.py
```

### Task 1: `write_system_meta`

Complete this function:

```python
def write_system_meta(self, payload: dict[str, Union[str, int, None]]) -> None:
```

This function should write ingest status into the `system_meta` table.

The setup is already done for you:

```python
current = self.get_system_meta()
next_payload = {**current, **payload}

with self._connect() as conn:
    raise NotImplementedError("Homework: write INSERT/UPDATE SQL for system_meta")
```

Replace the `raise NotImplementedError(...)` line with SQL code.

Required behavior:

- Store exactly one row in `system_meta`.
- The row should always use `id = 1`.
- If the row does not exist, insert it.
- If the row already exists, update it.
- Use values from `next_payload`.

The row should contain:

- `ingestion_status`
- `last_success_ingestion_time`
- `total_docs`

Hint: use SQLite upsert syntax:

```sql
ON CONFLICT(id) DO UPDATE SET
```

Expected SQL shape:

```python
conn.execute(
    """
    INSERT INTO system_meta (...)
    VALUES (...)
    ON CONFLICT(id) DO UPDATE SET
        ...
    """,
    (...),
)
```

### Task 2: `replace_chunk_metadata`

Complete this function:

```python
def replace_chunk_metadata(self, records: list[dict[str, Any]]) -> None:
```

This function should replace all rows in the `chunks` table after each ingest.

The setup is already done for you:

```python
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
```

Replace the `raise NotImplementedError(...)` line with SQL code.

Required behavior:

- Delete all existing rows from `chunks`.
- Insert all rows from the prepared `rows` list.
- Use `conn.executemany(...)` for batch insert.

Expected SQL shape:

```python
conn.execute("DELETE FROM chunks")
conn.executemany(
    """
    INSERT INTO chunks (...)
    VALUES (?, ?, ?, ?, ?)
    """,
    rows,
)
```

## SQLite Syntax You Need

### Connect And Auto-Close

Use the provided connection helper:

```python
with self._connect() as conn:
    ...
```

The `with` block makes sure the connection is handled safely.

### Execute One SQL Statement

Use `conn.execute(...)` for one SQL statement:

```python
conn.execute("DELETE FROM chunks")
```

### Use Parameterized SQL

Do not build SQL by manually formatting strings with user or record values.

Prefer placeholders:

```python
conn.execute(
    "INSERT INTO example (name, count) VALUES (?, ?)",
    ("demo", 3),
)
```

The `?` placeholders are filled by the tuple values.

This is safer and avoids SQL injection bugs.

### Insert Many Rows

Use `executemany` when inserting multiple rows:

```python
rows = [
    ("chunk_1", "doc_1"),
    ("chunk_2", "doc_1"),
]

conn.executemany(
    "INSERT INTO chunks (chunk_id, doc_id) VALUES (?, ?)",
    rows,
)
```

### Upsert With `ON CONFLICT`

SQLite can insert a row or update it if the primary key already exists:

```sql
INSERT INTO table_name (id, value)
VALUES (1, ?)
ON CONFLICT(id) DO UPDATE SET
    value = excluded.value
```

`excluded.value` means the new value you tried to insert.

## How To Test Manually

Start the backend:

```bash
cd backend
uvicorn app.main:app --reload
```

Check health:

```bash
curl -s http://127.0.0.1:8000/api/v1/health | python3 -m json.tool
```

Run ingest:

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool
```

Check health again:

```bash
curl -s http://127.0.0.1:8000/api/v1/health | python3 -m json.tool
```

After a successful implementation, `total_docs` and `last_success_ingestion_time` should reflect the ingest result.

## How To Inspect The SQLite File

The SQLite database file is:

```text
data/meta/rag.sqlite3
```

If you have the SQLite CLI installed, you can inspect it:

```bash
sqlite3 data/meta/rag.sqlite3
```

Inside the SQLite shell:

```sql
.tables
SELECT * FROM system_meta;
SELECT chunk_id, doc_id, source, chunk_index FROM chunks LIMIT 5;
.quit
```

## Common Mistakes

- Forgetting to delete old `chunks` rows before inserting new rows.
- Using string formatting instead of `?` placeholders.
- Forgetting that `system_meta` should only have one row with `id = 1`.
- Not using `ON CONFLICT(id) DO UPDATE`, which can cause duplicate insert errors.
- Inserting chunk columns in the wrong order.
- Removing the existing connection setup instead of using `self._connect()`.

## Success Criteria

Your implementation is complete when:

- `POST /api/v1/ingest` succeeds.
- `GET /api/v1/health` shows updated ingest metadata.
- `data/meta/rag.sqlite3` contains rows in `system_meta` and `chunks`.
- You did not change API response shapes.
- You did not rewrite the FAISS logic.
