from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file= REPO_ROOT / ".env", env_prefix="RAG_", extra="ignore")

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
    query_top_k: int = 1
    gemini_api_key: str | None = None
    gemini_model: str = "models/gemini-2.5-flash"
    llm_max_output_tokens: int = 256
    prompt_version: str = "v1"
    prompts_dir: Path = REPO_ROOT / "data/prompts"
    final_prompt_path: Path = REPO_ROOT / "data/prompts/final_prompt.txt"


settings = Settings()
