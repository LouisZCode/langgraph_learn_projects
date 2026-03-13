from tkinter import END
from unittest import result
from langgraph import graph
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class HelloWorldState(TypedDict):
    greeting : str

def hello_world_node(state: HelloWorldState):
    state["greeting"] = "Hello World" + state["greeting"]
    return state


builder = StateGraph(HelloWorldState)
builder.add_node("greet", hello_world_node)
builder.add_edge(START, "greet")
builder.add_edge("greet" , END)

graph = builder.compile()
result = graph.invoke({"greeting" : " from LangGraph"})

print(result)