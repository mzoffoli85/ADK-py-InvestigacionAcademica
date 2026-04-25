from ddgs import DDGS


def search_academic_sources(query: str) -> dict:
    """Search for academic and technical sources on a given topic using DuckDuckGo.

    Args:
        query: The search query string.

    Returns:
        A dict with 'results' (list of sources) or 'error' on failure.
    """
    try:
        with DDGS() as ddgs:
            hits = list(ddgs.text(query, max_results=5))

        results = [
            {
                "title": hit.get("title", ""),
                "url": hit.get("href", ""),
                "snippet": hit.get("body", ""),
            }
            for hit in hits
        ]
        return {"results": results, "count": len(results)}

    except Exception as e:
        return {"error": f"Search failed: {e}", "results": []}
