import json
from pathlib import Path

from datasets import load_dataset

OUTPUT_PATH = Path(__file__).with_name("wildchat_traffic_sample.json")

dataset = load_dataset("allenai/WildChat-1M", split="train", streaming=True)

test_records = []
target_samples = 2500

for entry in dataset:
    if entry.get("language") == "English" and entry.get("conversation"):
        first_user_turn = entry["conversation"][0]["content"]

        test_records.append(
            {
                "conversation_id": entry.get("conversation_hash"),
                "model_requested": entry.get("model", "gpt-4o-mini"),
                "prompt": first_user_turn,
                "turn_count": entry.get("turn"),
                "toxic": entry.get("toxic", False),
                "redacted": entry.get("redacted", False),
            }
        )

        if len(test_records) >= target_samples:
            break

with OUTPUT_PATH.open("w", encoding="utf-8") as f:
    json.dump(test_records, f, indent=2)

print(f"Extracted {len(test_records)} production test cases.")
