import os
import requests


def search_academic_sources(query: str) -> dict:
    """Search for academic and technical sources on a given topic.

    Args:
        query: The search query string.

    Returns:
        A dict with 'results' (list of sources) or 'error' on failure.
    """
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    if not api_key or not engine_id:
        return {
            "error": "Missing GOOGLE_SEARCH_API_KEY or GOOGLE_SEARCH_ENGINE_ID in environment.",
            "results": [],
        }

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": engine_id,
        "q": query,
        "num": 5,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = [
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
            for item in data.get("items", [])
        ]
        return {"results": results, "count": len(results)}

    except requests.RequestException as e:
        return {"error": f"Search request failed: {e}", "results": []}
    except Exception as e:
        return {"error": f"Unexpected error: {e}", "results": []}
