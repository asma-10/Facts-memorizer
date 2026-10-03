from pathlib import Path
import yaml

PROMPTS_FILE = Path(__file__).parent / "prompts.yaml"


def _load_data() -> dict:
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_system_prompt(version: str | None = None) -> str:
    """Return the system prompt text. Uses the active version if none is given."""
    data = _load_data()
    version = version or data["active_version"]

    try:
        return data["system_prompt"][version]["text"].strip()
    except KeyError:
        available = list(data["system_prompt"].keys())
        raise ValueError(f"Prompt version '{version}' not found. Available: {available}")


def list_versions() -> list[str]:
    """Return all version names, e.g. ['v1', 'v2']."""
    return list(_load_data()["system_prompt"].keys())


def get_active_version() -> str:
    """Return the version currently marked as active, e.g. 'v2'."""
    return _load_data()["active_version"]