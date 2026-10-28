"""Assistant & advisory engine (Epic 5)."""
import json

from .. import config, llm

SYSTEM = (
    "You are a construction advisor for residential and small commercial projects in India. "
    "Give practical, concise, safety-first advice. Mention relevant IS codes only when you are "
    "confident. Use the provided project context (site analysis, cost estimate) when present. "
    "State assumptions clearly and recommend a licensed engineer for structural decisions."
)


async def answer(question: str, context: dict | None) -> tuple[str, bool]:
    if config.DEMO_MODE:
        return (
            "DEMO MODE: set LLM_API_KEY to get real advice. "
            f"You asked: '{question}'. In general, verify curing time, rebar cover and "
            "load paths with your structural engineer before proceeding.",
            True,
        )
    user = question
    if context:
        user = f"Project context:\n{json.dumps(context, indent=2)}\n\nQuestion: {question}"
    return await llm.chat_text(SYSTEM, user), False
