from __future__ import annotations

from pathlib import Path
from typing import Any

from langchain_core.prompts import PromptTemplate

from app.core.config import settings


class PromptService:
    _SUPPORTED_VERSIONS = {"v1", "v2", "v3"}

    def build_and_persist_prompt(
        self,
        question: str,
        retrieved_chunks: list[dict[str, Any]],
    ) -> str:
        """Render selected prompt template with runtime values.

        Simplified class instruction:
        - Keep this service focused on template rendering + local persistence.
        - Build prompt only after `retrieved_chunks` are ready.
        - Placeholder mapping below is intentionally minimal for class demo.
        """
        prompt_version = settings.prompt_version.strip().lower()
        if prompt_version not in self._SUPPORTED_VERSIONS:
            raise ValueError(f"unsupported prompt_version: {settings.prompt_version}")

        template_path = settings.prompts_dir / f"query_prompt_{prompt_version}.md"
        template_text = template_path.read_text(encoding="utf-8")
        template = PromptTemplate.from_template(template_text)
        final_prompt = template.format(
            question=question,
            context_blocks=retrieved_chunks if retrieved_chunks else "(no retrieved context)",
        )

        self._ensure_parent_dir(settings.final_prompt_path)
        settings.final_prompt_path.write_text(final_prompt, encoding="utf-8")

        return final_prompt

    def _ensure_parent_dir(self, file_path: Path) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)


prompt_service = PromptService()
