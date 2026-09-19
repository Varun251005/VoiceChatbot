import requests
import json
import os

# Global flag to stop generation
_stop_generation = False


def stop_generation():
    """Set flag to stop generation"""
    global _stop_generation
    _stop_generation = True


def _call_ollama(user_text, timeout=300):
    url = "http://localhost:11434/api/generate"
    model_name = os.getenv("OLLAMA_MODEL", "qwen3.5:latest")
    payload = {"model": model_name, "prompt": user_text, "stream": False}
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
    except Exception:
        pass
    return ""


def _call_openai_fallback(user_text, api_key, model="gpt-3.5-turbo"):
    """Call OpenAI Chat Completions as a fallback when local Ollama is unavailable."""
    if not api_key:
        return ""

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": user_text}],
        "temperature": 0.7,
        "max_tokens": 512,
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            choices = data.get("choices") or []
            if choices:
                return choices[0].get("message", {}).get("content", "")
    except Exception:
        pass
    return ""


def get_llama_response(user_text, fallback_api_key=None):
    """
    Sends user text to local Ollama LLaMA API and returns response.
    If Ollama is unavailable and a fallback API key is provided (or found in
    `OPENAI_API_KEY` / `FALLBACK_OPENAI_API_KEY` env), calls OpenAI chat API.
    Returns: Response text (string) or empty string on failure.
    """
    global _stop_generation
    _stop_generation = False

    # Try local Ollama first
    text = _call_ollama(user_text)
    if _stop_generation:
        return ""

    if text:
        return text

    # Determine fallback key: explicit argument -> env var
    api_key = fallback_api_key or os.getenv("FALLBACK_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return ""

    # Call OpenAI as fallback
    return _call_openai_fallback(user_text, api_key)
