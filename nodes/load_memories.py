from graphs.states import State
from api.functions import get_memories

def load_memories(state: State) -> State:
    return {'matched_memory': get_memories(state["user_id"])}
