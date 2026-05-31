from __future__ import annotations

import json

from app.services.providers.gemini_client import GeminiClientError, gemini_client


class AnswerGenerationError(RuntimeError):
    pass


class GenerationService:
    def generate_answer(self, prompt: str) -> str:
        try:
            raw_output = gemini_client.generate_content(prompt)
        except GeminiClientError as exc:
            raise AnswerGenerationError(f"LLM generation failed: {exc}") from exc

        try:
            payload = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            raise AnswerGenerationError(
                "Model output is not valid JSON. Ensure prompt enforces strict JSON output."
            ) from exc

        if not isinstance(payload, dict):
            raise AnswerGenerationError("Model output JSON must be an object.")

        answer = payload.get("answer")
        if not isinstance(answer, str) or not answer.strip():
            raise AnswerGenerationError("Model output JSON must include non-empty 'answer' field.")

        return answer.strip()


generation_service = GenerationService()
