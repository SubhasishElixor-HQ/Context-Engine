"""Request text embeddings from a local Ollama server."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "embeddinggemma")


class EmbeddingServiceError(RuntimeError):
    """Raised when Ollama cannot return a usable embedding."""


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Get one numeric embedding vector for each input text."""
    if not texts:
        return []

    payload = json.dumps(
        {"model": OLLAMA_EMBED_MODEL, "input": texts}
    ).encode("utf-8")
    request = Request(
        f"{OLLAMA_BASE_URL}/api/embed",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise EmbeddingServiceError(
            "Could not reach Ollama. Start Ollama and check OLLAMA_BASE_URL."
        ) from exc

    vectors = result.get("embeddings")
    if not isinstance(vectors, list) or len(vectors) != len(texts):
        raise EmbeddingServiceError(
            "Ollama returned an invalid embedding response. Check the embedding model."
        )

    try:
        return [[float(value) for value in vector] for vector in vectors]
    except (TypeError, ValueError) as exc:
        raise EmbeddingServiceError(
            "Ollama returned an invalid embedding vector."
        ) from exc
