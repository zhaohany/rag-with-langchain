# Homework: CI Docker Build

## Goal

This project now has a GitHub Actions CI workflow (`.github/workflows/ci.yml`) with two jobs:

| Job | Status | Purpose |
|-----|--------|---------|
| `test` | **Working** | Runs unit tests on every PR and push to `main` |
| `build` | **Your task** | Validates that the backend can be packaged as a Docker image |

The `test` job is a completed example — it checks out the code, sets up Python, installs dependencies, and runs `make test-ci`. All four health tests pass.

The `build` job is defined in the workflow but **currently fails** because the project does not yet have a `Dockerfile`. Your task is to create one so the build job passes.

---

## What Is Docker?

Docker packages an application and its environment into a lightweight, reproducible image. Instead of manually installing Python and dependencies, you define the environment in a `Dockerfile` and Docker builds it for you.

Key concepts:

- **Image** — a snapshot of the app + its OS + dependencies (e.g., `rag-chatbot-backend:ci`)
- **Container** — a running instance of an image
- **Dockerfile** — a recipe file that describes how to build the image
- **Build context** — the directory Docker uses when building (the `.` in `docker build -t name:tag .`)

---

## What The CI Expects

The CI's `build` job runs:

```bash
docker build -t rag-chatbot-backend:ci .
```

The `.` means the build context is the repository root. Docker will look for a file named `Dockerfile` in that directory.

Your `Dockerfile` must:

1. Start from a Python 3.11 base image.
2. Set the working directory inside the container to `/app`.
3. Copy only `backend/requirements.txt` first and install dependencies (to leverage Docker layer caching).
4. Copy the rest of the `backend/` source code into the container.
5. Expose port 8000 (the port FastAPI listens on).
6. Set the default command to run the FastAPI server with uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Files To Read

Start with the CI workflow file to understand what it expects:

```text
.github/workflows/ci.yml
```

Then read the backend entry point to understand how the server starts:

```text
backend/app/main.py
```

---

## What Is Already Provided

Everything except the `Dockerfile` is already provided:

- The CI workflow (`.github/workflows/ci.yml`)
- The backend application code (`backend/`)
- All dependencies (`backend/requirements.txt`)

You only need to create **one file**: `Dockerfile` at the project root.

---

## How To Test Locally

### 1. Build the image

```bash
docker build -t rag-chatbot-backend:ci .
```

If the build succeeds, you will see output ending with something like:

```
=> => naming to docker.io/library/rag-chatbot-backend:ci
```

### 2. Run a container

```bash
docker run -p 8000:8000 rag-chatbot-backend:ci
```

### 3. Test the health endpoint

In another terminal:

```bash
curl -s http://127.0.0.1:8000/api/v1/health | python3 -m json.tool
```

You should see a JSON response with `"status": "ok"`.

### 4. Stop the container

Press `Ctrl+C` in the terminal where the container is running.

---

## Dockerfile Reference

### Base Image

```dockerfile
FROM python:3.11-slim
```

The `-slim` variant is smaller than the full `python:3.11` image and is sufficient for this project.

### Working Directory

```dockerfile
WORKDIR /app
```

All subsequent commands will run inside `/app`.

### Install Dependencies (with caching)

Copy only the requirements file first, then install. This way, Docker caches the pip install layer — if `requirements.txt` hasn't changed, Docker reuses the cached layer instead of reinstalling.

```dockerfile
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

### Copy Application Code

```dockerfile
COPY backend/ .
```

This copies the entire `backend/` directory contents into `/app` inside the container.

### Expose Port

```dockerfile
EXPOSE 8000
```

This documents which port the application uses (it does not publish the port — that is done with `-p` at runtime).

### Default Command

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The `CMD` instruction specifies what runs when the container starts.

### Check Your Dockerfile Doesn't Copy Unnecessary Files

Docker uses `.dockerignore` to exclude files from the build context. Create a `.dockerignore` at the project root if the image contains files it should not:

```text
.git/
.venv/
__pycache__/
data/
docs/
frontend/
mlops/
plans/
```

---

## Expected Dockerfile Layout

Place the `Dockerfile` at the project root (same directory as `README.md`, `.github/`, `backend/`):

```text
rag-with-langchain/
  .github/
    workflows/
      ci.yml
  backend/
    app/
    tests/
    requirements.txt
    Makefile
  Dockerfile          <-- create this
  README.md
  ...
```

---

## Success Criteria

Your implementation is complete when:

- `docker build -t rag-chatbot-backend:ci .` succeeds from the project root.
- The CI `build` job passes on GitHub when you push your branch.
- `docker run -p 8000:8000 rag-chatbot-backend:ci` starts the server.
- `curl http://127.0.0.1:8000/api/v1/health` returns `{"status": "ok", ...}`.
- You did not modify `backend/` application code or the CI workflow.
- You did not change the CI workflow expectations.

---

## Common Mistakes

- Putting the `Dockerfile` inside `backend/` instead of the project root.
- Forgetting the `.` at the end of `docker build`.
- Copying the entire repository into the container when only `backend/` is needed.
- Installing dependencies after copying all files (slower and breaks caching).
- Using `python:3.11` instead of `python:3.11-slim` (unnecessarily large image).
- Forgetting to expose `--host 0.0.0.0` in the uvicorn command (container will not be reachable).
- Adding the `requirements.txt` copy step incorrectly so the pip install fails because it cannot find the file.
