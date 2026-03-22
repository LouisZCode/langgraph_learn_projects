from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

load_dotenv()

#other options:
#   nvidia/nemotron-3-super-120b-a12b:free
#    stepfun/step-3.5-flash:free

model = ChatOpenRouter(
    model="nvidia/nemotron-3-super-120b-a12b:free",
)

response = model.invoke("Hello! can you explain to me what you can do and what you are good at?")
print(response.content)