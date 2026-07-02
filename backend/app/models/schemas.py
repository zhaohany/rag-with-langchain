from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    ingestion_status: str
    last_success_ingestion_time: Optional[str]
    total_docs: int


class IngestRequest(BaseModel):
    pass


class IngestResponse(BaseModel):
    status: str
    total_docs: int
    total_chunks: int
    message: str
    job_id: Optional[str] = None


class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class RetrievedChunk(BaseModel):
    chunk_id: str
    doc_id: str
    score: float
    text: str
    source: str


class QueryResponse(BaseModel):
    answer: Optional[str] = None
    used_top_k: int
    retrieved_chunks: list[RetrievedChunk]


class NotImplementedResponse(BaseModel):
    status: str
    message: str
