import asyncio
import os
import sys

# Set env BEFORE any project imports so config picks it up
os.environ["TAVILY_API_KEY"] = "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"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.web_search import web_search
from config import settings


async def test_tavily_search():
    """Test Tavily web_search with Chinese and English queries."""
    assert settings.tavily_api_key, "TAVILY_API_KEY should be loaded from env"
    print(f"Loaded TAVILY_API_KEY: {settings.tavily_api_key[:10]}...")

    # Test 1: Chinese query
    print("=" * 60)
    print("Test 1: Chinese query - 四姑娘山 徒步 天气")
    result = await web_search.ainvoke({"query": "四姑娘山 徒步 天气"})
    print(result[:600])
    assert "未配置" not in result, f"Config error: {result}"
    assert "http" in result, f"Result should contain URLs: {result[:200]}"
    print("PASS")

    # Test 2: English query
    print("=" * 60)
    print("Test 2: English query - Mount Siguniaya hiking weather")
    result = await web_search.ainvoke({"query": "Mount Siguniaya hiking weather"})
    print(result[:600])
    assert "未配置" not in result, f"Config error: {result}"
    assert "http" in result, f"Result should contain URLs: {result[:200]}"
    print("PASS")

    # Test 3: Missing API key
    print("=" * 60)
    print("Test 3: Missing API key")
    old_key = settings.tavily_api_key
    settings.tavily_api_key = ""
    result = await web_search.ainvoke({"query": "test"})
    print(result)
    assert "未配置" in result, f"Expected config error but got: {result}"
    settings.tavily_api_key = old_key
    print("PASS")

    print("=" * 60)
    print("All tests passed!")


if __name__ == "__main__":
    asyncio.run(test_tavily_search())
