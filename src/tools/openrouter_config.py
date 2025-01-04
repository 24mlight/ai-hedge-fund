import os
from openai import OpenAI


def get_openrouter_client():
    """Get OpenRouter client with the configured API key and base URL."""
    return OpenAI(
        base_url=os.environ.get(
            "OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


def get_chat_completion(messages, model=None):
    """Get chat completion from OpenRouter API."""
    client = get_openrouter_client()

    if model is None:
        model = os.environ.get(
            "OPENAI_MODEL", "google/gemini-2.0-flash-exp:free")

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        extra_headers={
            "HTTP-Referer": "http://localhost",  # Local development
            "X-Title": "AI Hedge Fund",  # App name
        }
    )

    return completion.choices[0].message.content
