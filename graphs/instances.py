from graphs.states import State
from langgraph.graph import StateGraph, START, END
from nodes.load_memories import load_memories
from nodes.chat import chat
from nodes.memorize import memorize
from nodes.save_if_needed import save_if_needed
from langgraph.checkpoint.memory import InMemorySaver

def build():
    graph_builder = StateGraph(State)

    graph_builder.add_node("load_memories", load_memories)
    graph_builder.add_node("chat", chat)
    graph_builder.add_node("memorize", memorize)
    graph_builder.add_node("save_if_needed", save_if_needed)

    graph_builder.add_edge(START, "load_memories")
    graph_builder.add_edge("load_memories", "chat")
    graph_builder.add_edge("chat", "memorize")
    graph_builder.add_edge("memorize", "save_if_needed")
    graph_builder.add_edge("save_if_needed", END)

    checkpointer = InMemorySaver()

    return graph_builder.compile(checkpointer=checkpointer)