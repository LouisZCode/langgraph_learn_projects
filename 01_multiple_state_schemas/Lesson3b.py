from langgraph import graph
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

class OverallState(TypedDict):
    partial_message:str
    user_input:str
    messages_output:str

class InputState(TypedDict):
    user_input : str

class OutputState(TypedDict):
    messages_output:str

class PrivateState(TypedDict):
    private_message:str

def add_world(state:InputState) -> OverallState:
    partial_answer = state['user_input'] + " World"
    print(f"Node 1 - add_world: Transformed '{state['user_input']}' to '{partial_answer}'")
 
    return {"partial_message" : partial_answer, "user_input": state["user_input"], "messages_output":""}

def add_exclamation(state:OverallState) -> OverallState:
    private_message = state["partial_message"] + "!"
    print(f"Node 2 - add_exclamation: Transformed '{state['partial_message']}' to '{private_message}'")

    return {"private_message" : private_message}

def finalize_message(state:PrivateState) -> OutputState:
    message_output = state["private_message"]
    print(f"Node 3 - finalize_message: Finalized message to '{message_output}'")

    return{"messages_output":message_output}

builder = StateGraph(OverallState, input=InputState, output=OutputState)
builder.add_node("add_world", add_world)
builder.add_node("add_exclamation", add_exclamation)
builder.add_node("finalize_message", finalize_message)

builder.add_edge(START, "add_world")
builder.add_edge("add_world", "add_exclamation")
builder.add_edge("add_exclamation", "finalize_message")
builder.add_edge("finalize_message", END)

graph = builder.compile()
graph.invoke({"user_input" : "Hello"})





#Code to visualize the graph, we will re-use this in all future lessons

from langchain_core.runnables.graph import MermaidDrawMethod
import random
import os
import subprocess
import sys

mermaid_png=graph.get_graph(xray=1).draw_mermaid_png(draw_method=MermaidDrawMethod.API) 

# Create an output folder if it doesn't exist, for now we can save in the current folder represented by .
output_folder = "."
os.makedirs(output_folder, exist_ok=True) 
filename = os.path.join(output_folder, f"graph_{random.randint(1, 100000)}.png") 
with open(filename, 'wb') as f:
    f.write(mermaid_png)
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', filename)) 
    elif sys.platform.startswith('linux'):
        subprocess.call(('xdg-open', filename))
    elif sys.platform.startswith('win'):
        os.startfile(filename)