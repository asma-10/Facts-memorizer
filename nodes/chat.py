from graphs.states import State
from config.llm import llm
from config.prompt_loader import load_system_prompt

def chat(state: State):
    user_message = state["user_message"]
    memories = state["matched_memory"]

    memory_text = "\n".join(str(m) for m in memories) if memories else "No known facts yet."

    message = [
        {'role': 'system', 'content': load_system_prompt("v1")},
        {'role': 'user', 'content': user_message}
    ]

    response = llm.invoke(message)
    return {'answer': response.content}