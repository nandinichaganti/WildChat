"""Routing policy helpers for model selection and fallback behavior."""

from __future__ import annotations

from typing import Dict, List


class ModelRouter:
    """Simple tenant-aware routing layer for demonstration purposes."""

    def __init__(self, route_map: Dict[str, List[str]] | None = None):
        self.route_map = route_map or {
            "analytics-team": ["gpt-4o-mini", "claude-3-haiku"],
            "core-banking-service": ["gpt-4o-mini"],
        }

    def select_model(self, tenant_id: str, requested_model: str | None = None) -> str:
        allowed = self.route_map.get(tenant_id, ["gpt-4o-mini"])
        if requested_model and requested_model in allowed:
            return requested_model
        return allowed[0]
