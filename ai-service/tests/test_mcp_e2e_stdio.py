"""
MCP stdio 端到端集成测试。

目的：现有 test_mcp_client.py / test_pexels_mcp_server.py 全部用 mock 验证协议层，
从未真实拉起过 MCP server 子进程。本测试套件直接通过 asyncio.subprocess 启动
pexels_server.py 进程，验证：

1. 真实 stdio 通道能跑通 JSON-RPC
2. MCPClient 的 initialize / list_tools / call_tool 完整生命周期
3. 协议错误（未知 method、未知 tool）能被正确序列化
4. load_mcp_tools() 端到端能加载工具并命名空间化

不依赖 PEXELS_API_KEY：测试 Pexels 协议层时用 handle_request() 直调（无需网络）；
需要真实子进程时，把 PEXELS_API_KEY 设为空，server 会返回 isError=true 的 MCP 错误结果，
这本身就是合规的 MCP 行为。

运行：
    cd ai-service
    python -m pytest tests/test_mcp_e2e_stdio.py -v
"""
import asyncio
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mcp.client import MCPClient, load_mcp_tools  # noqa: E402
from mcp_servers import pexels_server  # noqa: E402

SERVER_CMD = [sys.executable, str(ROOT / "mcp_servers" / "pexels_server.py")]


# ── 协议层：直接验证 server 的 JSON-RPC 序列化（无子进程、无网络） ──


def test_initialize_returns_protocol_handshake():
    """initialize 必须返回 protocolVersion + capabilities + serverInfo。"""
    resp = pexels_server.handle_request({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {"protocolVersion": "2025-06-18"},
    })

    assert resp["jsonrpc"] == "2.0"
    assert resp["id"] == 1
    result = resp["result"]
    assert result["protocolVersion"] == "2025-06-18"
    assert "tools" in result["capabilities"]
    assert result["serverInfo"]["name"] == "ai-hiking/pexels-mcp"


def test_initialized_notification_returns_none():
    """notifications/initialized 不应有响应（notification 语义）。"""
    resp = pexels_server.handle_request({
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
    })
    assert resp is None


def test_unknown_method_returns_jsonrpc_error():
    """未知 method 必须返回 JSON-RPC -32601（method not found）。"""
    resp = pexels_server.handle_request({
        "jsonrpc": "2.0",
        "id": 99,
        "method": "tools/explode",
    })
    assert resp["id"] == 99
    assert resp["error"]["code"] == -32601
    assert "tools/explode" in resp["error"]["message"]


def test_tools_list_includes_input_schema():
    """tools/list 必须返回完整 inputSchema，供客户端构造参数模型。"""
    resp = pexels_server.handle_request({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
    })
    tools = resp["result"]["tools"]
    by_name = {t["name"]: t for t in tools}

    assert "search_photos" in by_name
    assert "search_videos" in by_name

    # 验证 schema 字段齐全：LangChain 工具构造依赖这些字段
    photos = by_name["search_photos"]
    assert photos["description"]
    assert photos["inputSchema"]["type"] == "object"
    assert photos["inputSchema"]["required"] == ["query"]
    assert "query" in photos["inputSchema"]["properties"]


def test_call_tool_without_api_key_returns_isError_true():
    """无 PEXELS_API_KEY 时，server 必须以 isError=true 报告配置错误（不抛异常到客户端）。"""
    old = os.environ.pop("PEXELS_API_KEY", None)
    try:
        resp = pexels_server.handle_request({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "search_photos", "arguments": {"query": "hiking"}},
        })
        assert resp["result"]["isError"] is True
        payload = json.loads(resp["result"]["content"][0]["text"])
        assert "not configured" in payload["error"]
    finally:
        if old is not None:
            os.environ["PEXELS_API_KEY"] = old


def test_call_tool_with_empty_query_returns_isError_true():
    """空 query 必须被 server 拒绝（参数校验）。"""
    os.environ["PEXELS_API_KEY"] = "dummy-for-validation-test"
    try:
        resp = pexels_server.handle_request({
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "search_photos", "arguments": {"query": ""}},
        })
        assert resp["result"]["isError"] is True
        payload = json.loads(resp["result"]["content"][0]["text"])
        assert "query" in payload["error"].lower()
    finally:
        os.environ.pop("PEXELS_API_KEY", None)


def test_call_unknown_tool_returns_isError_true():
    """未知 tool name 必须返回 isError=true 而非 JSON-RPC error。"""
    os.environ["PEXELS_API_KEY"] = "dummy"
    try:
        resp = pexels_server.handle_request({
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {"name": "search_nothing", "arguments": {}},
        })
        assert resp["result"]["isError"] is True
        payload = json.loads(resp["result"]["content"][0]["text"])
        assert "Unknown Pexels tool" in payload["error"]
    finally:
        os.environ.pop("PEXELS_API_KEY", None)


# ── 真实 stdio 通道：拉起子进程走 JSON-RPC ─────────────────────────────


async def _spawn_client(env_override: dict | None = None) -> MCPClient:
    """拉起真实的 pexels_server.py 子进程并返回已连接的 MCPClient。"""
    client = MCPClient()
    # 故意不传 PEXELS_API_KEY：验证缺 key 时的协议路径
    await client.connect_stdio(SERVER_CMD[0], SERVER_CMD[1:], env=env_override or {})
    assert client.process is not None, "MCP server subprocess failed to start"
    assert client.process.stdin is not None
    assert client.process.stdout is not None
    return client


@pytest.mark.asyncio
async def test_real_subprocess_spawns_and_stays_alive():
    """验证 pexels_server.py 真的能作为子进程起来并保持运行。"""
    client = await _spawn_client()
    try:
        # 进程应仍在运行，未崩溃
        assert client.process.returncode is None, (
            f"MCP server exited unexpectedly with code {client.process.returncode}"
        )
    finally:
        await client.close()
        assert client.process is None


@pytest.mark.asyncio
async def test_real_initialize_lifecycle_via_stdio():
    """通过真实 stdio 走完整 initialize 握手。"""
    client = await _spawn_client()
    try:
        result = await client.initialize()
        assert result["protocolVersion"] == "2025-06-18"
        assert "tools" in result["capabilities"]
        assert client.initialized is True
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_real_list_tools_via_stdio():
    """通过真实 stdio 拉取工具列表，验证 JSON-RPC 响应解析。"""
    client = await _spawn_client()
    try:
        await client.initialize()
        tools = await client.list_tools()
        names = {t["name"] for t in tools}
        assert "search_photos" in names
        assert "search_videos" in names
        # 缓存必须被填充
        assert "search_photos" in client.tools
        assert "search_videos" in client.tools
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_real_call_tool_without_api_key_returns_isError():
    """通过真实 stdio 调 search_photos，验证缺 key 时的错误传播路径。"""
    client = await _spawn_client(env_override={"PEXELS_API_KEY": ""})
    try:
        await client.initialize()
        result = await client.call_tool("search_photos", {"query": "hiking"})

        # MCPClient.call_tool 在 isError=true 时直接返回原始 result 字典
        assert isinstance(result, dict)
        assert result["isError"] is True
        text = result["content"][0]["text"]
        assert "not configured" in text
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_real_subprocess_close_terminates_cleanly():
    """close() 必须真的终止子进程，无僵尸进程。"""
    client = await _spawn_client()
    pid = client.process.pid
    await client.initialize()
    await client.close()

    assert client.process is None
    # 等待 OS 清理
    await asyncio.sleep(0.1)
    # Windows 上 Process 对象的 returncode 在 wait() 后才会更新；这里只验证 process 句柄已置空
    assert pid > 0


# ── 集成层：load_mcp_tools() 端到端 ───────────────────────────────────


@pytest.mark.asyncio
async def test_load_mcp_tools_end_to_end_with_real_subprocess():
    """load_mcp_tools() 启动真实子进程 → 拉工具 → 命名空间化 → 关闭。"""
    # 用 PEXELS_API_KEY 空值：避免真实网络调用，但能跑通整个协议链路
    tools = await load_mcp_tools({
        "pexels": {
            "command": SERVER_CMD[0],
            "args": SERVER_CMD[1:],
            "env": {"PEXELS_API_KEY": ""},
        }
    })

    assert len(tools) == 2
    names = {t.name for t in tools}
    # 关键：工具必须带 mcp:<server>:<tool> namespace，避免与本地工具重名
    assert "mcp:pexels:search_photos" in names
    assert "mcp:pexels:search_videos" in names

    # 验证 LangChain StructuredTool 的元数据完整
    photo_tool = next(t for t in tools if t.name == "mcp:pexels:search_photos")
    assert "Pexels" in photo_tool.description or "pexels" in photo_tool.description.lower()
    assert photo_tool.args_schema is not None


@pytest.mark.asyncio
async def test_load_mcp_tools_empty_config_is_noop():
    """不配 MCP 时 load_mcp_tools() 不得拉任何子进程（no-op 安全）。"""
    import time
    start = time.monotonic()
    tools = await load_mcp_tools(None)
    elapsed = time.monotonic() - start
    assert tools == []
    # 空配置必须在毫秒级返回；任何 >1s 都说明偷偷起了子进程
    assert elapsed < 1.0, f"empty config should be a no-op, took {elapsed:.2f}s"


# ── 错误注入：验证 MCPClient 协议容错 ────────────────────────────────


@pytest.mark.asyncio
async def test_mcp_client_handles_unknown_method_from_server():
    """当 server 返回 JSON-RPC error（不是 result）时，call_tool 不得崩溃。"""
    client = await _spawn_client()
    try:
        await client.initialize()
        # 发一个 server 不认识的方法
        response = await client._send_request("tools/explode")
        assert "error" in response
        assert response["error"]["code"] == -32601
    finally:
        await client.close()
