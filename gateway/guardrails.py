"""Guardrail checks for input safety and tenant policy enforcement."""

from __future__ import annotations


BLOCKED_KEYWORDS = {
    "hack",
    "jailbreak",
    "bypass",
    "exploit",
    "drop table",
}


def is_blocked_prompt(prompt: str) -> bool:
    normalized = prompt.lower()
    return any(keyword in normalized for keyword in BLOCKED_KEYWORDS)
