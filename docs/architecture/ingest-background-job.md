# Ingest Background Job

## 概述

`POST /api/v1/ingest` 改为异步 background job 模式。API 不再同步执行 embedding，而是通过 FastAPI `BackgroundTasks` 将 ingestion pipeline 放入后台执行。

## 流程

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

## 关键设计

- 使用 FastAPI 内置 `BackgroundTasks`（不是 Celery / Redis 队列）。
- 一次 `/ingest` 请求 = 一个 job，全量重建本地索引。
- 若已有 `queued` 或 `running` 的 job，返回 `409 Conflict`。
- Job 状态存储在 SQLite `ingest_jobs` 表中。

## 文件改动

| 文件 | 改动 |
|---|---|
| `app/api/routes/ingest.py` | 改为使用 `BackgroundTasks` + `IngestQueueService` |
| `app/services/ingest_queue_service.py` | 新增：队列编排层 |
| `app/services/database_store.py` | 新增 `ingest_jobs` 表和 CRUD 方法 |
| `app/models/schemas.py` | `IngestResponse` 增加 `job_id` 字段 |

## Student Homework

### Task 1: `database_store.py` — `create_ingest_job`

补全 SQL 列名，让 INSERT 语句正确写入 `ingest_jobs` 表。

### Task 2: `ingest_queue_service.py` — `process_ingest_job`

替换 `raise NotImplementedError(...)` 为实际的 `self.ingest_service.run_sync_ingest()` 调用，并构建 success message。
