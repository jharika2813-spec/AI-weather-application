"""Groq-powered weather advice."""

import os

from groq import Groq


class GroqServiceError(Exception):
    """Raised when AI advice cannot be generated."""


def get_weather_advice(weather: dict) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise GroqServiceError("GROQ_API_KEY is not configured.")

    prompt = (
        "Give practical weather advice in two concise sentences. "
        f"Weather data: {weather}"
    )
    try:
        response = Groq(api_key=api_key).chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=120,
        )
        return response.choices[0].message.content.strip()
    except Exception as error:  # SDK errors vary by version.
        raise GroqServiceError("Unable to generate AI advice right now.") from error
