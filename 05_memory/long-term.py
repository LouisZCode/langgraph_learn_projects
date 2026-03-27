from langgraph.checkpoint.memory import InMemoryStore
from langgraph import graph
from langgraph.graph import StateGraph, MessagesState, START, END

import uuid

in_memory_store = InMemoryStore()

def store_user_info(state : MessagesState, config, *, store=in_memory_store):
    user_id = config["configurable"]["user_id"]
    Namespace = (user_id, "memories")

    memory_id = str(uuid.uuid4())
    memory = ("user_name" : state["user_name"])

    store.put(namespace.memory_id, memory)

    return {"messages" : ["User information saved"]}

def retrieve_user_information(state: MessagesState, config, *, store=in_memory_store):
    user_id = config["configurable"]["user_id"]
    namespace = (user_id, "memories")

    memories = store.search(namespace)

    if memories:
        info = f"Hello {memories[-1].value["user_name"]}, welcome back!"

    else:
        info = "I dont have enough information about you"

    return {"messages" , [info]}