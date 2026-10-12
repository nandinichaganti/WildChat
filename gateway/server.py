from __future__ import annotations

import time
from typing import List, Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from gateway.guardrails import is_blocked_prompt
from gateway.rate_limiter import TokenBucket

app = FastAPI(title="Aegis-AI Gateway")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: Optional[str] = "gpt-4o-mini"
    messages: List[Message]
    tenant_id: Optional[str] = "default"


REQUEST_COUNTER = 0
TENANT_BUCKETS = {
    "analytics-team": TokenBucket(capacity=100, refill_rate=5.0),
    "core-banking-service": TokenBucket(capacity=80, refill_rate=3.0),
}


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest, authorization: Optional[str] = Header(None)):
    global REQUEST_COUNTER
    REQUEST_COUNTER += 1

    prompt_text = req.messages[0].content.lower() if req.messages else ""
    tenant_id = req.tenant_id or "default"

    if is_blocked_prompt(prompt_text):
        raise HTTPException(
            status_code=403,
            detail="Policy Guardrail Violation: Input flagged as adversarial or restricted.",
        )

    bucket = TENANT_BUCKETS.setdefault(tenant_id, TokenBucket(capacity=50, refill_rate=2.0))
    if not bucket.consume(1):
        raise HTTPException(
            status_code=429,
            detail="Rate Limit Exceeded: Tenant token bucket depleted.",
        )

    time.sleep(0.05)
    return {
        "id": "chatcmpl-test-123",
        "object": "chat.completion",
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": f"Mock response for tenant {tenant_id}"},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 15, "completion_tokens": 10, "total_tokens": 25},
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("gateway.server:app", host="127.0.0.1", port=8000, reload=True)
