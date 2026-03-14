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
    pass