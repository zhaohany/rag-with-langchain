# Homework: Dockerize The RAG App

## Goal

In this homework, you will package the backend and frontend into Docker containers, then run the full local stack with Docker Compose.

You will complete the missing backend Docker instructions yourself. The frontend Dockerfile is already finished and can be used as a reference.

## What You Will Build

The repository already contains:

- `backend/Dockerfile`
- `frontend/Dockerfile`
- `backend/.dockerignore`
- `frontend/.dockerignore`
- `docker-compose.yml`

The frontend Dockerfile is complete and is provided as a reference example.

The backend Dockerfile is partially complete. Your main job is to fill in the backend `TODO` sections.

The Compose stack includes:

- FastAPI backend on `http://127.0.0.1:8000`
- React frontend served by nginx on `http://127.0.0.1:8080`
- PostgreSQL database on `127.0.0.1:5432`

Important: the current backend still uses SQLite for metadata. The Postgres service is included so you can practice multi-container networking and prepare for a future database migration. It is not automatically used by the backend unless you add Postgres support in the application code.

## Files To Read First

Start with these files:

```text
backend/Dockerfile
frontend/Dockerfile
docker-compose.yml
```

Do not copy template files. The Docker files have already been created in their final locations.

## Task 1: Backend Dockerfile

Open:

```text
backend/Dockerfile
```

Complete the TODO sections in this file:

- Copy `requirements.txt` into the image.
- Install Python dependencies.
- Copy the `app/` directory into the image.
- Add the `CMD` that starts FastAPI with uvicorn.

Requirements:

- The container must listen on `0.0.0.0`.
- The backend must expose port `8000`.
- The app import path is `app.main:app`.

Expected test:

```bash
docker build -t rag-backend ./backend
docker run --rm -p 8000:8000 rag-backend
```

Then open:

```text
http://127.0.0.1:8000/api/v1/health
```

## Task 2: Frontend Dockerfile

Open:

```text
frontend/Dockerfile
```

This file is already complete. Use it as a reference for Dockerfile structure and layer caching.

Notice that it:

- Copies `package.json` and `package-lock.json` first.
- Installs Node dependencies.
- Copies the rest of the frontend source.
- Builds the Vite production bundle.
- Copies the built `dist/` files into nginx.

Expected test:

```bash
docker build -t rag-frontend ./frontend
docker run --rm -p 8080:80 rag-frontend
```

Then open:

```text
http://127.0.0.1:8080
```

The standalone frontend container may not fully talk to the backend unless the backend is also running. That is expected.

## Task 3: Docker Compose

Open:

```text
docker-compose.yml
```

Review the three services:

- `postgres`
- `backend`
- `frontend`

Start the full stack:

```bash
docker compose up --build
```

Expected results:

- Frontend: `http://127.0.0.1:8080`
- Backend health endpoint: `http://127.0.0.1:8000/api/v1/health`
- Postgres port: `127.0.0.1:5432`

Stop the stack without deleting volumes:

```bash
docker compose down
```

## Task 4: Verify Postgres Persistence

The Compose file uses a named volume:

```yaml
volumes:
  postgres_data:
```

That volume is mounted into the Postgres container at:

```text
/var/lib/postgresql/data
```

Because of this, Postgres data survives normal stops and restarts.

Try this:

```bash
docker compose up -d postgres
docker compose exec postgres psql -U rag_user -d rag
```

Inside `psql`, run:

```sql
CREATE TABLE IF NOT EXISTS homework_notes (
    id SERIAL PRIMARY KEY,
    note TEXT NOT NULL
);

INSERT INTO homework_notes (note) VALUES ('docker volume test');

SELECT * FROM homework_notes;
```

Exit `psql`:

```text
\q
```

Now stop and restart:

```bash
docker compose down
docker compose up -d postgres
docker compose exec postgres psql -U rag_user -d rag -c "SELECT * FROM homework_notes;"
```

The row should still exist.

## When Is Postgres Data Deleted?

Stopping a container does not delete Postgres data.

Data is preserved when you run:

```bash
docker compose stop
docker compose down
docker compose up
```

Data is deleted if you remove the named volume, for example:

```bash
docker compose down -v
```

Data can also be deleted if you manually remove the volume:

```bash
docker volume rm rag-with-langchain_postgres_data
```

The exact volume name may differ depending on your project directory name. Check with:

```bash
docker volume ls
```

Summary:

- Stop container: data stays.
- Restart container: data stays.
- Remove container but keep named volume: data stays.
- Run `docker compose down -v`: data is deleted.
- Delete the volume manually: data is deleted.

## Submission Checklist

Submit the following files:

- `backend/Dockerfile`
- `frontend/Dockerfile`
- `backend/.dockerignore`
- `frontend/.dockerignore`
- `docker-compose.yml`

Also submit short answers to these questions:

- Why should Dockerfiles copy dependency files before application source files?
- Why must uvicorn bind to `0.0.0.0` inside a container?
- What is the difference between `docker compose down` and `docker compose down -v`?
- Why does the Compose file use a named volume for Postgres?

## Optional Challenge

Add real Postgres support to the backend.

Suggested direction:

- Add a Python Postgres driver such as `psycopg`.
- Add a `DATABASE_URL` setting.
- Create a Postgres-backed metadata store.
- Keep the existing SQLite behavior as the local default.
- Add tests that prove metadata can be written and read from Postgres.
