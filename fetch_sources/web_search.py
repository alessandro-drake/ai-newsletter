# fetch_sources/web_search.py

import os
import anthropic
from config import ANTHROPIC_API_KEY, SEARCH_QUERIES, MAX_ITEMS

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

MODEL = "claude-sonnet-4-20250514"
WEB_SEARCH_TOOL = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": MAX_ITEMS,  # allow up to MAX_ITEMS searches if you like
}

def fetch_web_search():
    """
    For each query in SEARCH_QUERIES, invoke Claude’s web_search tool once
    and return a list of dicts: { "query": ..., "results": [ {title, url, snippet, page_age}, … ] }.
    """
    all_results = []

    for query in SEARCH_QUERIES:
        resp = client.messages.create(
            model=MODEL,
            system="You are a search assistant. Use only the web_search tool and return its raw results.",
            messages=[{
                "role": "user",
                "content": (
                    f"Search the web for: {query}. "
                    "Return only the JSON array of results with keys: title, url, snippet, page_age."
                )
            }],
            tools=[WEB_SEARCH_TOOL],
            max_tokens=500,
        )

        extracted = []
        # Find the tool‐result block
        for block in resp.content:
            if getattr(block, "type", "") == "web_search_tool_result":
                for result in block.content:
                    if getattr(result, "type", "") == "web_search_result":
                        extracted.append({
                            "title":            getattr(result, "title", None),
                            "url":              getattr(result, "url", None),
                            "snippet":          getattr(result, "encrypted_content", None),
                            "page_age":         getattr(result, "page_age", None),
                        })
                break

        all_results.append({"query": query, "results": extracted})

    return all_results
