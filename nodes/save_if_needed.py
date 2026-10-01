from graphs.states import State
from api.functions import save_memory

def save_if_needed(state: State):
    fact = state["fact_to_save"]
    if not fact:
        return {}
    if isinstance(fact, list):
        for f in fact:
            save_memory(state["user_id"], f)
    else:
        save_memory(state["user_id"], fact)
    return {}