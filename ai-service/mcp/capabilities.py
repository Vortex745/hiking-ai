"""MCP-backed hiking capability resolver."""

from __future__ import annotations

import json
from typing import Any

from config import settings
from mcp.runtime import get_mcp_runtime


def _unavailable(capability: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "source": f"mcp.{capability}",
        "message": message,
    }


async def resolve_hiking_capability(capability: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Resolve a hiking capability through configured MCP tools."""
    server_configs = getattr(settings, "mcp_servers", {}) or {}
    capability_map = getattr(settings, "mcp_capability_map", {}) or {}
    if not server_configs:
        return _unavailable(capability, f"MCP 未配置，无法使用 {capability} 能力。")
    if capability not in capability_map:
        return _unavailable(capability, f"MCP capability map 未配置 {capability} 能力。")
    target = capability_map[capability]
    server = target.get("server") if isinstance(target, dict) else None
    tool = target.get("tool") if isinstance(target, dict) else None
    if not server or not tool:
        return _unavailable(capability, f"MCP capability map 中 {capability} 缺少 server 或 tool。")

    # Apply parameter mapping if configured
    param_map = target.get("param_map") if isinstance(target, dict) else None
    mapped_args = _apply_param_map(arguments, param_map)

    result = await get_mcp_runtime().call_tool(server, tool, mapped_args)
    if isinstance(result, dict) and result.get("isError"):
        return _unavailable(capability, str(result.get("message") or result))

    payload = _extract_payload(result)
    envelope: dict[str, Any] = {
        "ok": True,
        "source": f"mcp:{server}:{tool}",
    }
    if isinstance(payload, dict):
        envelope.update(payload)
    else:
        envelope["raw_result"] = payload
    return envelope


def _apply_param_map(arguments: dict[str, Any], param_map: dict[str, str] | None) -> dict[str, Any]:
    """Remap argument keys according to param_map.

    param_map format: {"source_key": "target_key"}.
    Only keys present in param_map are renamed; others are dropped.
    Values that are None are omitted from the output.

    When param_map is empty/falsy, a smart default is applied:
    - latitude + longitude are merged into "location" as "lng,lat"
    - other keys are passed through as-is (None values dropped)
    """
    if not param_map:
        mapped: dict[str, Any] = {}
        lat = arguments.get("latitude")
        lng = arguments.get("longitude")
        if lat is not None and lng is not None:
            mapped["location"] = f"{lng},{lat}"
        for k, v in arguments.items():
            if k in ("latitude", "longitude"):
                continue
            if v is not None:
                mapped[k] = v
        return mapped
    mapped = {}
    for src, tgt in param_map.items():
        val = arguments.get(src)
        if val is not None:
            mapped[tgt] = val
    return mapped


def _extract_payload(result: Any) -> Any:
    content = result.get("content") if isinstance(result, dict) else result
    if isinstance(content, list) and content:
        first = content[0]
        if isinstance(first, dict) and "text" in first:
            text = first.get("text") or ""
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
    return result
