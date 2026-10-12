import json
import random
from pathlib import Path

from locust import HttpUser, between, task

DATA_PATH = Path(__file__).with_name("wildchat_traffic_sample.json")

with DATA_PATH.open("r", encoding="utf-8") as f:
    TRAFFIC_DATA = json.load(f)


class GuardrailBlockedException(Exception):
    """Raised when an adversarial prompt is blocked (HTTP 403)."""


class RateLimitThrottledException(Exception):
    """Raised when a tenant exceeds token budget / rate limit (HTTP 429)."""


class GatewayBackendException(Exception):
    """Raised on internal gateway server faults (HTTP 5xx)."""


class GatewayLoadTester(HttpUser):
    wait_time = between(0.1, 0.8)

    @task
    def send_chat_completion(self):
        sample = random.choice(TRAFFIC_DATA)
        payload = {
            "model": sample.get("model_requested", "gpt-4o-mini"),
            "messages": [{"role": "user", "content": sample["prompt"]}],
            "tenant_id": random.choice(["analytics-team", "core-banking-service"]),
        }
        headers = {
            "Authorization": "Bearer test-api-key-123",
            "Content-Type": "application/json",
        }

        with self.client.post(
            "/v1/chat/completions",
            json=payload,
            headers=headers,
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 403:
                response.success()
                raise GuardrailBlockedException(f"Tenant blocked by guardrail: {response.text}")
            elif response.status_code == 429:
                response.success()
                raise RateLimitThrottledException(f"Tenant throttled by token bucket: {response.text}")
            else:
                response.failure(f"HTTP {response.status_code}")
                raise GatewayBackendException(f"Unhandled gateway status: {response.status_code}")
