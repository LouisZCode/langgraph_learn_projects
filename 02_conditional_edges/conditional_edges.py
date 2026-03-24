
from langgraph import graph
from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict

class GreetingState(TypedDict):
    greeting : str

def normalize_greeting_node(state : GreetingState) -> GreetingState:
    state['greeting'] = state['greeting'].lower()
    return state

def hi_greeting_node(state:GreetingState):
    state['greeting'] = "Hi there " + state['greeting']
    return state

def regular_greeting_node(state:GreetingState):
    state['greeting'] = "Hello " + state['greeting']
    return state

def choose_greeting_node(state:GreetingState):
    return "hi_greeting_node" if "hi" in state['greeting'] else "regular_greeting_node"


builder = StateGraph(GreetingState)
builder.add_node("normalize_greeting_node", normalize_greeting_node)
builder.add_node("hi_greeting_node", hi_greeting_node)
builder.add_node("regular_greeting_node", regular_greeting_node)

builder.add_edge(START, "normalize_greeting_node")

builder.add_conditional_edges(
    "normalize_greeting_node", choose_greeting_node, ["hi_greeting_node", "regular_greeting_node"]
)

builder.add_edge("hi_greeting_node", END)
builder.add_edge("regular_greeting_node", END)

graph = builder.compile()

result = graph.invoke({"greeting" : "Hey sir how are you?"})

print(result)


"""
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
"""