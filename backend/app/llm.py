"""Thin client for a Meta LLaMA (vision + text) model behind an OpenAI-compatible API."""
import base64
import json
import re

import httpx

from . import config


class LLMError(RuntimeError):
    pass


def _extract_json(text: str) -> dict:
    """Pull the first JSON object out of a model reply (handles ```json fences)."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise LLMError("Model did not return JSON")
    return json.loads(match.group(0))


async def _chat(messages: list[dict], temperature: float = 0.2, max_tokens: int = 1200) -> str:
    headers = {"Authorization": f"Bearer {config.LLM_API_KEY}"}
    payload = {
        "model": config.LLM_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    async with httpx.AsyncClient(timeout=90) as client:
        resp = await client.post(f"{config.LLM_BASE_URL}/chat/completions", headers=headers, json=payload)
    if resp.status_code != 200:
        raise LLMError(f"LLM request failed ({resp.status_code}): {resp.text[:300]}")
    return resp.json()["choices"][0]["message"]["content"]


async def chat_text(system: str, user: str) -> str:
    return await _chat([
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ], temperature=0.4)


async def vision_json(system: str, prompt: str, image_bytes: bytes, mime: str) -> dict:
    b64 = base64.b64encode(image_bytes).decode()
    content = [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
    ]
    reply = await _chat([
        {"role": "system", "content": system},
        {"role": "user", "content": content},
    ])
    return _extract_json(reply)
