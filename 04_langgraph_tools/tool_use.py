from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode

from langgraph import graph
from langgraph.graph import END, START, MessagesState, StateGraph

from agent import model
from tavily import TavilyClient

@tool
def search_the_web(query : str):
    """Tool to search the web and get information in real time about current topics on the web"""
    tavily_client = TavilyClient()
    response = tavily_client.search(query)
    return response

tool_node = ToolNode([search_the_web], handle_tool_errors=False)
model = model.bind_tools([search_the_web])

def call_llm(state:MessagesState):
    messages = state["messages"]
    response = model.invoke(messages[-1].content)
    return {"messages": [response]}

def call_tool(state:MessagesState):
    return "tools" if state["messages"][-1].tool_calls else END

builder = StateGraph(MessagesState)
builder.add_node("call_llm", call_llm)
builder.add_node("tools", tool_node)

builder.add_edge(START, "call_llm")
builder.add_conditional_edges(
    "call_llm", call_tool, ["tools", END]
)
builder.add_edge("tools", "call_llm")

graph = builder.compile()

input_messsage = ({"messages" : [
    {"role": "system", "content" :"You answer all questions. If the question is recent, you use your tool. If it is not or generic, you just answer. You have access to real time information using your 'search_the_web' tool."},
    {"role" : "user", "content" : input("your message is:\n")}
    ]})


for i in graph.stream(input_messsage, stream_mode="values"):
    i["messages"][-1].pretty_print()










"""
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