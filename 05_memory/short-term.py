from langgraph.checkpoint.memory import InMemorySaver
from langgraph import graph
from langgraph.graph import END, START, StateGraph, MessagesState

from agent import model

system_message = {"role": "system", "content" :"You answer all questions. If the question is recent, you use your tool. If it is not or generic, you just answer. You have access to real time information using your 'search_the_web' tool. do not use markdown formatting (no **, no #, no *, etc.)."}

def call_llm(state : MessagesState):
    messages = state["messages"]
    response = model.invoke([system_message] + messages)
    return {"messages" : [response]}

checkpointer = InMemorySaver()

builder = StateGraph(MessagesState)
builder.add_node("call_llm", call_llm)

builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

graph = builder.compile(checkpointer=checkpointer)

while True:

    user_input = input("\nyour message is:\n")

    if user_input == "exit":
        break

    else:

        input_messsage = ({"messages" : [
            {"role" : "user", "content" : "{user_input}"}
            ]})

        #here we create the session id thet needt to be part of the 
        conf = {"configurable" : {"thread_id" : "session_1"}}

        for i in graph.stream(input_messsage, config=conf, stream_mode="values"):
            i["messages"][-1].pretty_print()