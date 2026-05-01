from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="RAG_")

    app_name: str = "rag-with-langchain"
    app_version: str = "0.1.0"
    env: str = "local"
    cors_origins: list[str] = ["http://127.0.0.1:5173", "http://localhost:5173"]
    system_meta_path: Path = REPO_ROOT / "data/system/system_meta.json"
    raw_docs_dir: Path = REPO_ROOT / "data/raw_docs"
    index_path: Path = REPO_ROOT / "data/index/faiss.index"
    metadata_path: Path = REPO_ROOT / "data/meta/metadata.json"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_batch_size: int = 32
    chunk_size: int = 800
    chunk_overlap: int = 120


settings = Settings()
