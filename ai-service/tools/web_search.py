import httpx
from langchain_core.tools import tool


@tool
async def web_search(query: str) -> str:
    """Search the web for current information. Use this when you need to find recent news, facts, or data."""
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()

            abstract = data.get("AbstractText", "")
            source = data.get("AbstractSource", "")
            heading = data.get("Heading", "")

            if abstract:
                result = f"标题: {heading}\n来源: {source}\n摘要: {abstract}"
            else:
                # Fallback to related topics
                topics = data.get("RelatedTopics", [])
                results = []
                for topic in topics[:5]:
                    if "Text" in topic:
                        results.append(topic["Text"])
                result = "\n".join(results) if results else f"未找到关于「{query}」的明确结果。"
            return result
    except Exception as e:
        return f"搜索出错: {str(e)}。请稍后重试。"
