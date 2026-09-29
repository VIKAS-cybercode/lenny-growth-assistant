import os

import requests
from openai import OpenAI


MODEL_PROVIDER = os.getenv(
    "MODEL_PROVIDER",
    "ollama",
).lower()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b",
)

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini",
)


def generate_with_provider(prompt: str) -> str:
    """
    Generate a response using the configured LLM provider.

    Supported providers:
    - ollama
    - openai
    """

    if MODEL_PROVIDER == "ollama":
        return _generate_with_ollama(prompt)

    if MODEL_PROVIDER == "openai":
        return _generate_with_openai(prompt)

    raise RuntimeError(
        f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}"
    )


def _generate_with_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            f"Ollama request timed out after 300 seconds "
            f"using model '{OLLAMA_MODEL}'"
        ) from exc

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            f"Could not connect to Ollama at {OLLAMA_URL}. "
            "Make sure Ollama is running."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Ollama request failed: {exc}"
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "Ollama returned an invalid JSON response"
        ) from exc

    answer = data.get("response")

    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError(
            "Ollama returned an empty response"
        )

    return answer.strip()


def _generate_with_openai(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured"
        )

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
        )

    except Exception as exc:
        raise RuntimeError(
            f"OpenAI request failed: {exc}"
        ) from exc

    answer = response.output_text

    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError(
            "OpenAI returned an empty response"
        )

    return answer.strip()