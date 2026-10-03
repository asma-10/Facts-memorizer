from graphs.states import State
from config.llm import llm
from config.prompt_loader import load_system_prompt


def format_memories(memories: list[dict]) -> str:
    if not memories:
        return "No known facts yet."
    return "\n".join(str(m) for m in memories)


def build_messages(system_prompt: str, memories: list[dict], user_message: str) -> list[dict]:
    memory_text = format_memories(memories)
    return [
        {
            "role": "system",
            "content": f"{system_prompt}\n\nKnown facts about the user:\n{memory_text}",
        },
        {"role": "user", "content": user_message},
    ]


def chat(state: State):
    messages = build_messages(
        load_system_prompt(), state["matched_memory"], state["user_message"]
    )
    response = llm.invoke(messages)
    return {"answer": response.content}