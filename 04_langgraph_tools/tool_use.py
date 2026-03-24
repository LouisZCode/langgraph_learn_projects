from langchain.tools import tool
from langgraph.prebuilt import ToolNode

from langgraph import graph
from langgraph.graph import END, START, MessagesState, StateGraph
from urllib3 import response

from agent import model
from tavily import TavilyClient


@tool
def search_the_web(query : str):
    """Tool to search the web and get information in real time about current topics on the web"""
    tavily_client = TavilyClient()
    response = tavily_client.search(query)
    return response

tool_node = ToolNode([search_the_web])
model = model.bind_tools([search_the_web])

def call_llm(state:MessagesState):
    messages = state["messages"]
    response = model.invoke(messages[-1].content)

    #capture the tool result
    if response.tool_calls:
        tool_result = tool_node.invoke({"messages": [response]})
    
        tool_message = tool_result["messages"][-1].content
    
        response.content += f"\nTool Result: {tool_message}"

    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node("call_llm", call_llm)

builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

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