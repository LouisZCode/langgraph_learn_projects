from langgraph import graph
from langgraph.graph import START, END, StateGraph, MessagesState
from agent import agent

def call_llm(state:MessagesState):
    messages = state["messages"]
    response = agent.invoke(messages[-1].content)
    return {"messages" : [response]}

builder = StateGraph(MessagesState)
builder.add_node("call_llm", call_llm)

builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

graph = builder.compile()

input_messsage = ({"messages" : [{"role" : "user", "content" : input("your message is:\n")}]})

for i in graph.stream(input_messsage, stream_mode="values"):
    i["messages"][-1].pretty_print()












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