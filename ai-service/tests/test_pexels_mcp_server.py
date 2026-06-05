import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx

from mcp_servers import pexels_server


class FakeResponse:
    headers = {
        "X-Ratelimit-Limit": "20000",
        "X-Ratelimit-Remaining": "19999",
        "X-Ratelimit-Reset": "3600",
    }

    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class FakeClient:
    calls = []

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None

    def get(self, url, *, params=None, headers=None):
        self.calls.append({"url": url, "params": params, "headers": headers})
        return FakeResponse({
            "page": 1,
            "per_page": 1,
            "total_results": 1,
            "next_page": "https://api.pexels.com/v1/search?page=2",
            "photos": [
                {
                    "id": 42,
                    "url": "https://www.pexels.com/photo/42/",
                    "photographer": "Alex Trail",
                    "photographer_url": "https://www.pexels.com/@alex",
                    "alt": "A mountain hiking trail",
                    "avg_color": "#334455",
                    "width": 1200,
                    "height": 800,
                    "src": {
                        "original": "https://images.pexels.com/photos/42/original.jpeg",
                        "large": "https://images.pexels.com/photos/42/large.jpeg",
                        "medium": "https://images.pexels.com/photos/42/medium.jpeg",
                    },
                }
            ],
        })


def test_list_tools_exposes_photo_and_video_search():
    response = pexels_server.handle_request({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
    })

    tools = response["result"]["tools"]
    assert [tool["name"] for tool in tools] == ["search_photos", "search_videos"]
    assert tools[0]["inputSchema"]["required"] == ["query"]


def test_search_photos_requires_api_key(monkeypatch):
    monkeypatch.delenv("PEXELS_API_KEY", raising=False)

    response = pexels_server.handle_request({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "search_photos", "arguments": {"query": "hiking"}},
    })

    assert response["result"]["isError"] is True
    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["error"] == "PEXELS_API_KEY is not configured"


def test_search_photos_calls_pexels_and_summarizes_results(monkeypatch):
    FakeClient.calls = []
    monkeypatch.setenv("PEXELS_API_KEY", "secret")
    monkeypatch.setattr(httpx, "Client", FakeClient)

    response = pexels_server.handle_request({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "search_photos",
            "arguments": {
                "query": "hiking trail",
                "per_page": 99,
                "orientation": "landscape",
            },
        },
    })

    assert response["result"]["isError"] is False
    call = FakeClient.calls[0]
    assert call["url"] == "https://api.pexels.com/v1/search"
    assert call["params"]["query"] == "hiking trail"
    assert call["params"]["per_page"] == 10
    assert call["params"]["orientation"] == "landscape"
    assert call["headers"]["Authorization"] == "secret"

    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["provider"] == "Pexels"
    assert payload["photos"][0]["id"] == 42
    assert payload["photos"][0]["attribution"] == "Photo by Alex Trail on Pexels"
