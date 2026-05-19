from fastapi import APIRouter

from agent.agent import AIAgent, validate_tool_configuration
from config import settings

tools_router = APIRouter(prefix="/tools")


def _mcp_configured() -> bool:
    return bool(getattr(settings, "mcp_servers", None))


def _external_keys_status() -> dict[str, bool]:
    return {
        "amap_api_key": bool(settings.amap_api_key),
        "openai_api_key": bool(settings.openai_api_key),
        "embedding_api_key": bool(settings.embedding_api_key),
        "rerank_api_key": bool(settings.rerank_api_key),
    }


@tools_router.get("")
async def list_tools(include_hidden: bool = False):
    registry = AIAgent.get_tool_registry()
    tools = registry.tools_api_response(include_hidden=include_hidden)
    return {
        "count": len(tools),
        "include_hidden": include_hidden,
        "tools": tools,
    }


@tools_router.get("/health")
async def tools_health():
    registry = AIAgent.get_tool_registry()
    visible = registry.list_tools(include_hidden=False)
    all_tools = registry.list_all_tools()
    configured = _mcp_configured()
    return {
        "status": "ok",
        "tools_total": len(all_tools),
        "visible_tools": len(visible),
        "hidden_tools": len(all_tools) - len(visible),
        "configuration": validate_tool_configuration(),
        "mcp": {
            "configured": configured,
            "loaded": False,
        },
        "external_keys": _external_keys_status(),
    }
