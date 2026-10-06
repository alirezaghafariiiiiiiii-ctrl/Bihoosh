import json
import urllib.parse
import urllib.request


class WebSearch:
    """
    جست‌وجوی مستقل اینترنت.
    فعلاً از SearXNG استفاده می‌کند.
    """

    def __init__(self, base_url="https://search.bus-hit.me"):
        self.base_url = base_url.rstrip("/")

    def search(self, query, limit=5):
        query = query.strip()

        if not query:
            return []

        params = urllib.parse.urlencode({
            "q": query,
            "format": "json",
            "language": "auto",
            "safesearch": 1
        })

        url = f"{self.base_url}/search?{params}"

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Bihoosh/0.1"
            }
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

            results = []

            for item in data.get("results", [])[:limit]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", "")
                })

            return results

        except Exception as error:
            return [{
                "title": "خطا در جست‌وجو",
                "url": "",
                "content": str(error)
            }]
