"""MCPClient JSON-RPC stdio 通信的单元测试（匹配真实 MCPClient API）"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from mcp.client import MCPClient


# ── 连接测试 ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_connect_stdio_success():
    """测试 connect_stdio 成功连接 MCP 服务器"""
    mock_process = AsyncMock()
    mock_process.stdin = AsyncMock()
    mock_process.stdout = AsyncMock()
    mock_process.stderr = AsyncMock()

    with patch("asyncio.create_subprocess_exec", new=AsyncMock(return_value=mock_process)):
        c = MCPClient()
        await c.connect_stdio("some-mcp-server", ["--port=1234"])

        assert c.process is not None
        assert c.process == mock_process
        assert c.tools == {}

        await c.close()


@pytest.mark.asyncio
async def test_connect_stdio_failure():
    """测试 connect_stdio 在命令不存在时静默容错（logger warning + 不抛异常）"""
    c = MCPClient()
    # FileNotFoundError 被捕获并写 warning，不抛异常
    with patch("asyncio.create_subprocess_exec", side_effect=FileNotFoundError("mcp not found")):
        await c.connect_stdio("nonexistent-server")
        # process 应为 None，表示连接失败
        assert c.process is None


# ── _send_request ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_send_request_sends_json_rpc_and_returns_response():
    """测试 _send_request 发送 JSON-RPC 请求并返回完整响应"""
    mock_stdin = AsyncMock()
    mock_stdout = AsyncMock()
    mock_stdout.readline = AsyncMock(
        return_value=(json.dumps({"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}) + "\n").encode()
    )

    mock_process = AsyncMock(spec=asyncio.subprocess.Process)
    mock_process.stdin = mock_stdin
    mock_process.stdout = mock_stdout

    c = MCPClient()
    c.process = mock_process

    response = await c._send_request("list_tools")

    assert response == {"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}
    # 验证发送了正确的 JSON-RPC 请求
    written_data = mock_stdin.write.call_args[0][0]
    sent = json.loads(written_data)
    assert sent["method"] == "list_tools"
    assert sent["jsonrpc"] == "2.0"
    assert sent["id"] == 1


@pytest.mark.asyncio
async def test_send_request_not_connected():
    """测试 _send_request 在未连接时抛出 ConnectionError"""
    c = MCPClient()
    c.process = None

    with pytest.raises(ConnectionError, match="MCP server not connected"):
        await c._send_request("list_tools")


@pytest.mark.asyncio
async def test_send_request_timeout():
    """测试 _send_request 在 readline 超时时抛出 asyncio.TimeoutError"""
    mock_stdin = AsyncMock()
    mock_stdout = AsyncMock()
    mock_stdout.readline = AsyncMock(side_effect=asyncio.TimeoutError)

    mock_process = AsyncMock(spec=asyncio.subprocess.Process)
    mock_process.stdin = mock_stdin
    mock_process.stdout = mock_stdout

    c = MCPClient()
    c.process = mock_process

    with pytest.raises(asyncio.TimeoutError):
        await c._send_request("list_tools")


# ── list_tools ─────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_tools_returns_tools_and_caches():
    """测试 list_tools 解析 result.tools 并缓存到 self.tools"""
    tools_data = [
        {"name": "web_search", "description": "Search the web", "inputSchema": {}},
        {"name": "calculator", "description": "Do math", "inputSchema": {}},
    ]

    c = MCPClient()
    with patch.object(c, "_send_request", new=AsyncMock(return_value={
        "result": {"tools": tools_data}
    })):
        result = await c.list_tools()

        assert result == tools_data
        # 检查缓存
        assert c.tools["web_search"]["name"] == "web_search"
        assert c.tools["calculator"]["name"] == "calculator"
        c._send_request.assert_awaited_once_with("list_tools")


@pytest.mark.asyncio
async def test_list_tools_empty_on_error():
    """测试 list_tools 在请求失败时返回空列表（logger warning）"""
    c = MCPClient()
    with patch.object(c, "_send_request", side_effect=ConnectionError("not connected")):
        result = await c.list_tools()
        assert result == []
        # tools 缓存不变
        assert c.tools == {}


# ── call_tool ──────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_call_tool_calls_mcp_and_returns_content():
    """测试 call_tool 调用正确方法并返回 content 列表"""
    expected_content = [{"type": "text", "text": "42"}]

    c = MCPClient()
    with patch.object(c, "_send_request", new=AsyncMock(return_value={
        "result": {"content": expected_content}
    })):
        result = await c.call_tool("calculator", {"expression": "6*7"})

        assert result == expected_content
        c._send_request.assert_awaited_once_with(
            "call_tool",
            {"name": "calculator", "arguments": {"expression": "6*7"}},
        )


@pytest.mark.asyncio
async def test_call_tool_error_returns_error_string():
    """测试 call_tool 在请求失败时返回错误字符串（logger error）"""
    c = MCPClient()
    with patch.object(c, "_send_request", side_effect=ConnectionError("not connected")):
        result = await c.call_tool("calculator")
        assert result == "MCP tool error: not connected"


# ── convert_to_langchain_tools ─────────────────────────────────────


@pytest.mark.asyncio
async def test_convert_to_langchain_tools_creates_decorated_tools():
    """测试 convert_to_langchain_tools 根据 self.tools 生成 @tool 函数"""
    c = MCPClient()
    c.tools = {
        "web_search": {
            "name": "web_search",
            "description": "搜索网络获取信息",
            "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}},
        }
    }

    lc_tools = c.convert_to_langchain_tools()
    assert len(lc_tools) == 1

    tool_fn = lc_tools[0]
    # @tool 装饰器产生的对象有 name / description / args 等属性
    assert tool_fn.name == "web_search"
    assert "搜索网络" in tool_fn.description
    # 调用该工具应委托到 call_tool
    with patch.object(c, "call_tool", new=AsyncMock(return_value='[{"type":"text","text":"result"}]')):
        result = await tool_fn.ainvoke({"query": "hello"})
        c.call_tool.assert_awaited_once_with("web_search", {"query": "hello"})


@pytest.mark.asyncio
async def test_convert_to_langchain_tools_empty():
    """测试空 tools 缓存返回空列表"""
    c = MCPClient()
    assert c.convert_to_langchain_tools() == []


@pytest.mark.asyncio
async def test_load_tools_from_config_returns_empty_when_disabled():
    """MCP 未配置时不应默认加载任何外部工具。"""
    from mcp.client import load_mcp_tools

    tools = await load_mcp_tools(None)

    assert tools == []


@pytest.mark.asyncio
async def test_load_tools_from_config_namespaces_loaded_tools():
    """显式配置 MCP 时，加载出的工具应带 server namespace，避免与本地工具重名。"""
    from mcp.client import load_mcp_tools

    mock_tool = MagicMock()
    mock_tool.name = "image_search"

    with patch.object(MCPClient, "connect_stdio", new=AsyncMock()), \
        patch.object(MCPClient, "list_tools", new=AsyncMock(return_value=[{
            "name": "image_search",
            "description": "Search images",
            "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}},
        }])), \
        patch.object(MCPClient, "convert_to_langchain_tools", return_value=[mock_tool]), \
        patch.object(MCPClient, "close", new=AsyncMock()):
        tools = await load_mcp_tools({
            "image": {
                "command": "python",
                "args": ["server.py"],
            }
        })

    assert len(tools) == 1
    assert tools[0].name == "mcp:image:image_search"


# ── close ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_close_terminates_process_and_waits():
    """测试 close 正确终止子进程"""
    mock_process = AsyncMock(spec=asyncio.subprocess.Process)
    mock_process.terminate = MagicMock()
    mock_process.wait = AsyncMock(return_value=0)

    c = MCPClient()
    c.process = mock_process

    await c.close()

    mock_process.terminate.assert_called_once()
    mock_process.wait.assert_awaited_once()
    assert c.process is None


@pytest.mark.asyncio
async def test_close_no_process():
    """测试 close 在没有进程时安全执行"""
    c = MCPClient()
    c.process = None
    await c.close()  # 不应抛出异常


@pytest.mark.asyncio
async def test_close_already_terminated():
    """测试 close 在进程已退出后不会重复 terminate（软安全）"""
    mock_process = AsyncMock(spec=asyncio.subprocess.Process)
    # returncode 非 None 表示已退出，但 terminate() 本身仍可调用（os 容错）
    mock_process.returncode = 0
    mock_process.terminate = MagicMock()
    mock_process.wait = AsyncMock(return_value=0)

    c = MCPClient()
    c.process = mock_process

    await c.close()
    # terminate 在已退出的进程上调用是安全的（os 层忽略），这里不做严格断言
    assert c.process is None
