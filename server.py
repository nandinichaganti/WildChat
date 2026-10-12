from fastapi import FastAPI, Header, HTTPException, Response
from pydantic import BaseModel
from typing import List, Optional
import time
import random

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: Optional[str] = "gpt-4o-mini"
    messages: List[Message]
    tenant_id: Optional[str] = "default"

# Simulated simple in-memory request counter for rate limiting
REQUEST_COUNTER = 0

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest, authorization: Optional[str] = Header(None)):
    global REQUEST_COUNTER
    REQUEST_COUNTER += 1

    prompt_text = req.messages[0].content.lower() if req.messages else ""

    # 1. Simulate an Input Guardrail trigger (HTTP 403)
    # Block queries containing sensitive keywords or flagged toxic patterns
    if any(keyword in prompt_text for keyword in ["hack", "jailbreak", "bypass", "exploit", "drop table"]):
        raise HTTPException(
            status_code=403,
            detail="Policy Guardrail Violation: Input flagged as adversarial or restricted."
        )

    # 2. Simulate Token / Rate Limit Throttling (HTTP 429)
    # Trip rate limit randomly or every 10th request to simulate bucket overflow
    if REQUEST_COUNTER % 10 == 0:
        raise HTTPException(
            status_code=429,
            detail="Rate Limit Exceeded: Tenant token bucket depleted."
        )

    # 3. Normal 200 OK Execution
    time.sleep(0.05)
    return {
        "id": "chatcmpl-test-123",
        "object": "chat.completion",
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": f"Mock response for tenant {req.tenant_id}"},
                "finish_reason": "stop"
            }
        ],
        "usage": {"prompt_tokens": 15, "completion_tokens": 10, "total_tokens": 25}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)