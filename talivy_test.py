from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


tavily_client = TavilyClient()
response = tavily_client.search("Who is Leo Messi?")

print(response)