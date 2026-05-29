from __future__ import annotations

try:
    from google import genai
    from google.genai import errors, types
except ImportError:  # pragma: no cover - depends on local optional install timing
    genai = None
    errors = None
    types = None

from app.core.config import settings


class GeminiClientError(RuntimeError):
    pass


class GeminiClient:
    def generate_content(self, prompt: str) -> str:
        """Homework: implement Gemini SDK call in the try block.

        Keep pre-validation and post-validation unchanged.
        Students should complete only the API invocation block.
        """
        if not isinstance(prompt, str) or not prompt.strip():
            raise GeminiClientError("Prompt must be a non-empty string.")

        api_key = settings.gemini_api_key
        if not api_key:
            raise GeminiClientError(
                "Gemini API key is missing. Set RAG_GEMINI_API_KEY in your .env or environment."
            )
        if genai is None or errors is None or types is None:
            raise GeminiClientError(
                "google-genai is not installed. Run `pip install -r backend/requirements.txt`."
            )

        try:
            # TODO(homework): implement Gemini API call.
            raise NotImplementedError("Homework: implement Gemini API call in gemini_client.py")
        except errors.APIError as exc:
            raise GeminiClientError(f"Gemini API error: {exc}") from exc
        except Exception as exc:
            raise GeminiClientError(f"Gemini request failed: {exc}") from exc

        text = response.text
        if not isinstance(text, str) or not text.strip():
            raise GeminiClientError("Gemini returned empty text output.")

        return text


gemini_client = GeminiClient()
