import json
import os

MEMORY_FILE = "memories.json"

def _load_all() -> dict:
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def get_memories(user_id: str) -> list[dict]:
    data = _load_all()
    return data.get(user_id, [])

def save_memory(user_id: str, fact: dict):
    data = _load_all()
    data.setdefault(user_id, []).append(fact)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)