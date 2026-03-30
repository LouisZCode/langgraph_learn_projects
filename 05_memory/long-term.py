from dotenv import load_dotenv
from langgraph.store.postgres import PostgresStore
from langgraph import graph
from langgraph.graph import StateGraph, MessagesState, START, END

from langchain_core.tools import tool

import os
from agent import model
import uuid

load_dotenv()
database = os.getenv("DATABASE_URL")

with PostgresStore.from_conn_string(database) as pg_store:
    pg_store.setup()

    @tool                                                                                                                           
    def add_to_memory(memory_name: str, memory_value: str):                                                         
        """Save a personal detail about the user"""
        user_id = conf["configurable"]["user_id"]
        namespace = (user_id, "memories")                                                                                           
        memory_id = str(uuid.uuid4())                                                                                               
        pg_store.put(namespace, memory_id, {memory_name: memory_value})                                                             
        return "Memory saved"

    model = model.bind_tools([add_to_memory])

    system_message = {"role": "system", "content" :"You answer all questions. If the question is recent, tell the user you have no recent info. If it is not or generic, you just answer. do not use markdown formatting (no **, no #, no *, etc.)."}
    review_system_message = {"role": "system", "content" :"Your goal is to review the user messages and find any personal preference or life event or project. any personal detail is also important. All this is in goal of personalization. If you find any personal preference, event or information, save it using your 'add_to_memory' tool. do not use markdown formatting (no **, no #, no *, etc.)."}

    def call_llm(state : MessagesState):
        messages = state["messages"]
        response = model.invoke([system_message] + messages)
        return {"messages" : [response]}

    def llm_review(state : MessagesState):
        messages = state["messages"][-1]   #should be the last message sent by the user
        response = model.invoke([review_system_message] + [messages])
        if response.tool_calls:
            for tool_call in response.tool_calls:                                                                                   
                add_to_memory.invoke(tool_call["args"])                                                                           
                                                                                                                                
        return {"messages": []}  # don't pollute the conversation 

    def retrieve_user_information(state: MessagesState, config, *, store=pg_store):
        user_id = config["configurable"]["user_id"]
        namespace = (user_id, "memories")
        memories = store.search(namespace)

        if memories:
            info = "\n".join([str(m.value) for m in memories])
        else:
            info = "No memories found for this user"
        return {"messages": [{"role": "system", "content": info}]}


    builder = StateGraph(MessagesState)
    builder.add_node("call_llm", call_llm)
    builder.add_node("retrieve_user_info", retrieve_user_information)
    builder.add_node("llm_review", llm_review)


    builder.add_edge(START, "retrieve_user_info")
    builder.add_edge("retrieve_user_info" , "call_llm")

    builder.add_edge(START, "llm_review")
    builder.add_edge("llm_review", END)

    builder.add_edge("call_llm", END)

    graph = builder.compile(store=pg_store)

    user_input = input("\nyour message is:\n")

    input_messsage = ({"messages" : [
        {"role" : "user", "content" : f"{user_input}"}
        ]})

    #Here we can pass the user that is "logged in"
    conf = {"configurable" : {"thread_id" : "session_1", "user_id" : "luis_123"}}

    seen = 0                                                                                                                             
    for i in graph.stream(input_messsage, config=conf, stream_mode="values"):                                                          
        new_msgs = i["messages"][seen:]
        for msg in new_msgs:                                                                                                             
            msg.pretty_print()
        seen = len(i["messages"]) 


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