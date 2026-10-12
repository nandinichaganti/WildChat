# WildChat Load Test

This repo is a small load-testing setup for an AI gateway using real-ish WildChat-style prompts.

## What it does

- Pulls a filtered sample from the WildChat dataset
- Saves a compact JSON file with prompts and metadata
- Uses Locust to generate synthetic traffic against a local API endpoint
- Simulates chat-completion requests that look like real gateway traffic

## Files

- `load_data.py`: builds the sample dataset from the WildChat corpus
- `wildchat_traffic_sample.json`: generated prompt dataset used for testing
- `assess_traffic.py`: Locust test class that posts to `/v1/chat/completions`
- `locustfile.py`: simple entry point so Locust can run the test file directly

## Typical flow

1. Generate the sample dataset
2. Start the local app or gateway at `http://localhost:8000`
3. Run Locust against the target host

```bash
python load_data.py
locust -f locustfile.py --host http://localhost:8000
```

## Why this is useful

It gives you a lightweight way to test API behavior under load without needing a huge production dataset. The script is designed to mimic realistic prompt traffic and check how the gateway responds to bursty traffic patterns.
