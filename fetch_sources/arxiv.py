# fetch_sources/arxiv.py

import requests
import feedparser
import logging
import sys
import os

# Add the project root directory to the Python path
# This allows importing 'config' from the parent directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
from config import ARXIV_CATEGORIES, MAX_ITEMS # noqa: E402

ARXIV_API_URL = "https://export.arxiv.org/api/query"

def fetch_arxiv():
    """
    Query arXiv for the latest papers in each category.
    Returns a list of dicts (id, title, authors, summary, published, link).
    """
    # 1) Clean up categories
    cats = [cat.strip() for cat in ARXIV_CATEGORIES if cat.strip()]
    cat_query = "+OR+".join(f"cat:{cat}" for cat in cats)

    params = {
        "search_query": cat_query,
        "start": 0,
        "max_results": MAX_ITEMS,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    headers = {
        "User-Agent": "ai-newsletter/0.1 (github.com/alessandro-drake/ai-newsletter)"
    }

    # 2) Fetch with proper headers
    # FIX: Increase the timeout to 30 seconds to be more resilient
    resp = requests.get(ARXIV_API_URL, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    logging.debug(f"arXiv API URL: {resp.url}")
    logging.debug(f"arXiv API status code: {resp.status_code}")
    logging.debug(f"arXiv API response snippet: {resp.text[:200].replace(chr(10), ' ')}")

    # 3) Parse feed
    feed = feedparser.parse(resp.content)
    if feed.bozo:
        logging.warning(f"Error parsing arXiv feed: {feed.bozo_exception}")
        return []
    
    if not feed.entries:
        logging.warning("arXiv API query returned 0 paper entries.")
        logging.debug(f"Feed details (feed.feed): {feed.feed}") # opensearch:totalResults might be here
        logging.debug(f"Full raw XML response from arXiv: {resp.text}") # Log the full small response
        return []

    papers = []
    for entry in feed.entries:
        try:
            papers.append({
                "id":        getattr(entry, 'id', 'N/A'),
                "title":     getattr(entry, 'title', 'N/A').strip().replace("\n", " "),
                "authors":   [getattr(a, 'name', 'N/A') for a in getattr(entry, 'authors', [])],
                "summary":   getattr(entry, 'summary', 'N/A').strip().replace("\n", " "),
                "published": getattr(entry, 'published', 'N/A'),
                "link":      getattr(entry, 'link', 'N/A'),
            })
        except AttributeError as e:
            logging.warning(f"Skipping entry due to missing attribute: {e} - Entry: {entry}")
            continue
    return papers

if __name__ == "__main__":
    # This block runs only when the script is executed directly
    # (not when imported as a module)
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    print("Fetching arXiv papers...")
    papers_data = fetch_arxiv()
    print(f"Fetched {len(papers_data)} papers.")
    # You can print more details if you want, e.g., the first paper
    if papers_data:
        print("First paper:", papers_data[0])