from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent

load_dotenv()

#other options:
#   nvidia/nemotron-3-super-120b-a12b:free
#    stepfun/step-3.5-flash:free

model = ChatOpenRouter(
    model="nvidia/nemotron-3-super-120b-a12b:free",
)

agent = create_agent(                                                                                                            
    model=model,                                                                                                        
    system_prompt="You answer with no preambles and all in plain texts with spaces. do not use markdown formatting (no **, no #, no *, etc.)."
    )

"""
response = agent.invoke(
    {
        "messages" : {
            "role" : "user", 
            "content" : "Hello! can you explain to me what you can do and what you are good at?"
            }
    }
    )

for i, msg in enumerate(response["messages"]):
    msg.pretty_print()
"""