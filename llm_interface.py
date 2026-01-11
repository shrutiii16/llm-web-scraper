import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from scraper import scrape_website
load_dotenv()
KEY = os.getenv("GROQ_API_KEY")
if not KEY:
    raise RuntimeError("GROQ_API_KEY not found in .env")
MODEL = os.getenv("LLM_MODEL")
if not MODEL:
    raise RuntimeError("LLM_MODEL not found in .env")
llm = ChatGroq(api_key=KEY,model=MODEL,temperature=0)
llm = llm.bind_tools([scrape_website])
print("\nLLM Scraper Tool")
url = input("Enter URL: ").strip()
prompt = f"Use the scrape_website tool to scrape this URL: {url}"
res = llm.invoke(prompt)
if hasattr(res, "tool_calls") and res.tool_calls:
    for c in res.tool_calls:
        if c["name"] == "scrape_website":
            scrape_website.invoke(c["args"]["url"])
else:
    print("LLM did not call tool")
