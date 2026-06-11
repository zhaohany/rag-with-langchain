from __future__ import annotations

from typing import Any, Optional

from langchain_community.vectorstores import FAISS

from app.core.config import settings
from app.services.generation_service import generation_service
from app.services.prompt_service import prompt_service
from app.shared.embedding import get_embedding_model


class QueryService:
    def run_query(self, question: str) -> dict[str, Any]:
        """Run retrieval flow and persist a final prompt example.

        Input:
        - `question`: user question string.

        Output:
        - dict with:
          - `used_top_k`: int
          - `retrieved_chunks`: list[dict[str, Any]]

        Current scope:
        1) Embed the question with the preloaded embedding model.
        2) Retrieve top-k chunks from local FAISS.
        3) Normalize retrieved chunks for the API response.
        4) Build `context_blocks` from normalized chunks (example strategy).
        5) Render prompt template with `{context_blocks}` + `{question}` and
           persist to `data/prompts/final_prompt.txt`.

        Out of scope:
        - LLM answer generation
        - Multi-turn memory
        """
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("question must not be empty")

        top_k = settings.query_top_k
        if top_k <= 0:
            raise ValueError("query_top_k must be greater than 0")
        store = self._load_vector_store()
        matches = store.similarity_search_with_score(normalized_question, k=top_k)

        retrieved_chunks: list[dict[str, Any]] = []
        for doc, raw_score in matches:
            retrieved_chunks.append(self._build_retrieved_chunk(doc.page_content, doc.metadata, raw_score))

        prompt = prompt_service.build_and_persist_prompt(
            question=normalized_question,
            retrieved_chunks=retrieved_chunks,
        )
        answer = generation_service.generate_answer(prompt)

        return {"answer": answer, "used_top_k": top_k, "retrieved_chunks": retrieved_chunks}

    def _load_vector_store(self) -> FAISS:
        index_dir = str(settings.index_path.parent)
        index_name = settings.index_path.stem
        return FAISS.load_local(
            folder_path=index_dir,
            embeddings=get_embedding_model(),
            index_name=index_name,
            allow_dangerous_deserialization=True,
        )

    def _build_retrieved_chunk(
        self,
        text: str,
        metadata: Optional[dict[str, Any]],
        raw_score: float,
    ) -> dict[str, Any]:
        """Normalize one retrieved result for API response.

        Input:
        - `text`: retrieved chunk text (`Document.page_content`)
        - `metadata`: retrieved metadata (`Document.metadata`)
        - `raw_score`: FAISS similarity/distance score

        Required output (must match `RetrievedChunk` schema):
        - `chunk_id: str`
        - `doc_id: str`
        - `score: float`
        - `text: str`
        - `source: str`

        Rules:
        1) Never return missing keys.
        2) Always cast values to expected types.
        3) Use safe defaults when metadata keys are absent.
        4) Keep result deterministic and JSON-serializable.
        """
        metadata = metadata or {}
        chunk_id = str(metadata.get("chunk_id", ""))
        doc_id = str(metadata.get("doc_id", ""))
        score = round(raw_score, 3)
        source = str(metadata.get("source", ""))

        return {
            "chunk_id": chunk_id,
            "doc_id": doc_id,
            "score": score,
            "text": text,
            "source": source,
        }

query_service = QueryService()
