"""OpenAI client factory for the LangGraph nodes."""

from __future__ import annotations

import os

from langchain_openai import ChatOpenAI

DEFAULT_MODEL = "gpt-4o-mini"


def get_chat_model(temperature: float = 0.0) -> ChatOpenAI:
    """Build a ChatOpenAI client.

    The project's ``.env`` uses ``OPENAI_KEY``; langchain expects
    ``OPENAI_API_KEY``. We map it here if needed.
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_KEY (or OPENAI_API_KEY) is not set. "
            "Copy .env.example to .env and fill it in."
        )

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    return ChatOpenAI(model=model, temperature=temperature, api_key=api_key)
