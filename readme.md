# Enterprise AI Gateway & Policy Proxy (Aegis-AI)

An asynchronous, high-throughput AI Gateway built with FastAPI, Redis, and Locust to enforce edge-level guardrails, multi-tenant rate limits, and latency optimization for large language model workloads.

---

## 🚀 Key Architectural Features

- Asynchronous Proxy Layer: Standardizes OpenAI-compatible /v1/chat/completions endpoints across distributed backend services.
- Circuit Breakers & Input Guardrails: Intercepts adversarial prompts, jailbreak patterns, and unauthorized queries before firing downstream LLM calls (HTTP 403).
- Multi-Tenant Token Governance: Enforces tenant-based rate limits and token quotas via a token-bucket algorithm, mitigating runaway API billing (HTTP 429).
- Traffic Benchmarking Suite: Evaluated under high-concurrency real-world prompt distributions extracted from AllenAI's WildChat dataset.

---

## 📊 Benchmark Results (Locust Load Test)

Tested with concurrent virtual users streaming requests against the gateway:

| Metric | Baseline (Uncached) | Guardrail / Throttled Interceptions |
| :--- | :--- | :--- |
| Median Latency | ~2,100 ms | < 15 ms |
| p95 Latency | ~4,050 ms | < 25 ms |
| Token Savings | 0% | 100% tokens spared on blocked traffic |

> Interception of adversarial queries and depleted token buckets occurs entirely at the gateway boundary, preventing resource exhaustion on upstream model providers.

---

## 🛠️ Tech Stack

- API Engine: Python, FastAPI, Uvicorn, Pydantic
- Performance & Load Testing: Locust, AllenAI WildChat-1M Dataset
- Telemetry & Tracing: Custom HTTP status metrics, OpenTelemetry-ready spans
- Deployment: Docker, Docker Compose

---

## 🚦 Getting Started

### 1. Installation

```bash
git clone https://github.com/nandinichaganti/WildChat.git
cd WildChat
pip install -r requirements.txt
```

### 2. Run the Gateway Server

```bash
python -m gateway.server
```

The server starts on http://127.0.0.1:8000.

### 3. Run the Locust Load Testing Suite

```bash
locust -f benchmarks/assess_traffic.py --host http://127.0.0.1:8000
```

Open http://localhost:8089 to monitor real-time throughput, latency percentiles, and exceptions.

---

## 📁 Repository Structure

```text
WildChat/
├── gateway/
│   ├── __init__.py
│   ├── server.py
│   ├── router.py
│   ├── guardrails.py
│   └── rate_limiter.py
├── benchmarks/
│   ├── __init__.py
│   ├── assess_traffic.py
│   ├── ingest_wildchat.py
│   └── wildchat_traffic_sample.json
├── configs/
│   └── tenants.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

