from pathlib import Path
import yaml

PROMPTS_FILE = Path(__file__).parent / "prompts.yaml"


def load_system_prompt(version: str | None = None) -> str:
    """Return the system prompt text. Uses the active version if none is given."""
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    version = version or data["active_version"]

    try:
        return data["system_prompt"][version]["text"].strip()
    except KeyError:
        available = list(data["system_prompt"].keys())
        raise ValueError(f"Prompt version '{version}' not found. Available: {available}")