from langgraph import graph
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
import random
from langchain_core.runnables.graph import MermaidDrawMethod
import os
import subprocess
import sys

class HelloWorldState(TypedDict):
    greeting : str

def hello_world_node(state: HelloWorldState):
    state["greeting"] = "Hello World" + state["greeting"]
    return state

def exclamation_node(state: HelloWorldState):
    state["greeting"] += "!"
    return state


#Graph
builder = StateGraph(HelloWorldState)
builder.add_node("greet", hello_world_node)
builder.add_node("exclaim", exclamation_node)
#Logic
builder.add_edge(START, "greet")
builder.add_edge("greet", "exclaim")
builder.add_edge("exclaim" , END)
# Add
graph = builder.compile()
result = graph.invoke({"greeting" : " from LangGraph"})

print(result)












#Code to visualize the graph, we will re-use this in all future lessons

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