import os
import requests
import urllib.parse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
load_dotenv()
TOKEN = os.getenv("SCRAPEDO_TOKEN")
if not TOKEN:
    raise RuntimeError("SCRAPEDO_TOKEN not found in .env")
BASE = os.getenv("SCRAPEDO_BASE_URL")
if not BASE:
    raise RuntimeError("SCRAPEDO_BASE_URL missing")
def fetch(url: str) -> str:
    u = urllib.parse.quote(url)
    api = f"{BASE}?url={u}&token={TOKEN}&super=true&render=true&block_resources=true"
    r = requests.get(api, timeout=90)
    r.raise_for_status()
    return r.text
def clean(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        t.decompose()
    text = soup.get_text("\n", strip=True)
    return "\n".join(l for l in text.splitlines() if l.strip())

@tool
def scrape_website(url: str) -> str:
    """Scrape a webpage and print its clean text content."""
    print(f"\nScraping: {url}\n")
    html = fetch(url)
    text = clean(html)
    print(text)
    return "Done"
