from graphs.states import State
from config.llm import llm
import json


def memorize(state: State):
    user_message = state["user_message"]
    message = [
        {'role': 'system', 'content': "You are an agent that decides whether the user message contains a fact worth memorizing. If yes, extract it and return ONLY valid JSON, no extra text, no markdown. Format: {\"fact\": \"...\"}. If multiple facts, return a JSON list: [{\"fact\": \"...\"}, {\"fact\": \"...\"}]. If no fact, return {}."},
        {'role': 'user', 'content': f"Extract the fact from this message: {user_message}"}
    ]
    response = llm.invoke(message)
    raw = response.content.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        fact = json.loads(raw)
    except json.JSONDecodeError:
        try:
            fact = json.loads(f"[{raw}]")
        except json.JSONDecodeError:
            print(f"[memorize] Failed to parse: {raw}")
            fact = {}
    return {'fact_to_save': fact}
