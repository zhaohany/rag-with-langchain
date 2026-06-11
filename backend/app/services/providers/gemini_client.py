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
        """Generate answer JSON with Gemini after validating local configuration."""
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
            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    top_p=0.5,
                    max_output_tokens=1024,
                    response_mime_type="application/json",
                    response_schema={
                        "type": "object",
                        "properties": {
                            "answer": {"type": "string"}
                        },
                        "required": ["answer"]
                    }
                )
            )
        except errors.APIError as exc:
            raise GeminiClientError(f"Gemini API error: {exc}") from exc
        except Exception as exc:
            raise GeminiClientError(f"Gemini request failed: {exc}") from exc

        text = response.text
        if not isinstance(text, str) or not text.strip():
            raise GeminiClientError("Gemini returned empty text output.")

        return text


gemini_client = GeminiClient()
