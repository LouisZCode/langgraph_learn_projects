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
    partial_answer = state['user_input'] + "World"
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