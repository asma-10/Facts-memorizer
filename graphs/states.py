from typing import TypedDict

class State(TypedDict):
    user_id: str
    user_message: str
    matched_memory: list[dict]
    fact_to_save: dict
    answer: str