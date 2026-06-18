# Homework: complete the backend Dockerfile TODO sections.

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install Python dependencies first so Docker can cache this layer.
# TODO 1: Copy requirements.txt into the image.
# Hint: the destination can be ./requirements.txt

# TODO 2: Install dependencies from requirements.txt.
# Hint: use python -m pip install --upgrade pip, then pip install -r requirements.txt

# Copy the backend application code.
# TODO 3: Copy the app/ directory into /app/app.

# Keep runtime data outside the source tree inside the container.
RUN mkdir -p /app/data/raw_docs /app/data/index /app/data/meta /app/data/system /app/data/prompts

ENV RAG_RAW_DOCS_DIR=/app/data/raw_docs \
    RAG_INDEX_PATH=/app/data/index/faiss.index \
    RAG_METADATA_PATH=/app/data/meta/metadata.json \
    RAG_DATABASE_PATH=/app/data/meta/rag.sqlite3 \
    RAG_SYSTEM_META_PATH=/app/data/system/system_meta.json \
    RAG_PROMPTS_DIR=/app/data/prompts \
    RAG_FINAL_PROMPT_PATH=/app/data/prompts/final_prompt.txt

EXPOSE 8000

# TODO 4: Start the FastAPI app with uvicorn.
# Requirements:
# - bind to 0.0.0.0, not 127.0.0.1
# - listen on port 8000
# Hint command shape: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
