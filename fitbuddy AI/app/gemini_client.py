from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@lru_cache(maxsize=1)
def get_client():

    api_key = os.getenv(
        "GEMINI_API_KEY",
        ""
    ).strip()

    if not api_key:
        return None

    from google import genai

    return genai.Client(
        api_key=api_key
    )


def generate_text(
    prompt: str,
    model: str
) -> str:

    client = get_client()

    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()