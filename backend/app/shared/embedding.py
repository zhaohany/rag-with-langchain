from __future__ import annotations

import os
from importlib import import_module
from typing import Any

from app.core.config import settings

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("KMP_INIT_AT_FORK", "FALSE")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

_embedding_model: Any = None


def preload_embedding_model() -> None:
    global _embedding_model
    if _embedding_model is None:
        try:
            sentence_transformers = import_module("sentence_transformers")
        except ImportError as exc:
            raise RuntimeError("sentence-transformers is not installed") from exc
        SentenceTransformer = getattr(sentence_transformers, "SentenceTransformer")
        _embedding_model = SentenceTransformer(settings.embedding_model_name)


def get_embedding_model() -> Any:
    if _embedding_model is None:
        raise RuntimeError("Embedding model is not preloaded")
    return _embedding_model


def embed_texts(texts: list[str], batch_size: int) -> list[list[float]]:
    if not texts:
        return []
    model = get_embedding_model()
    vectors = model.encode(texts, batch_size=max(batch_size, 1), convert_to_numpy=True)
    return vectors.tolist()
