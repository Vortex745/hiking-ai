import asyncio
import inspect
import json
import logging
from typing import Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel

logger = logging.getLogger("ai-service.mcp")


class MCPClient:
    """Client for connecting to MCP servers via stdio transport.

    Implements basic JSON-RPC MCP protocol for tool discovery and execution.
    """

    def __init__(self):
        self.process: asyncio.subprocess.Process | None = None
        self.tools: dict[str, dict] = {}

    async def connect_stdio(self, command: str, args: list[str] | None = None):
        """Connect to an MCP server via stdio."""
        if args is None:
            args = []
        try:
            self.process = await asyncio.create_subprocess_exec(
                command,
                *args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            logger.info(f"MCP client connected: {command} {' '.join(args)}")
        except FileNotFoundError:
            logger.warning(f"MCP server not found: {command}")
        except Exception as e:
            logger.error(f"MCP connection failed: {e}")

    async def _send_request(self, method: str, params: dict | None = None) -> dict:
        """Send a JSON-RPC request to the MCP server."""
        if not self.process or not self.process.stdin:
            raise ConnectionError("MCP server not connected")

        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {},
        }

        write_result = self.process.stdin.write((json.dumps(request) + "\n").encode())
        if inspect.isawaitable(write_result):
            await write_result
        await self.process.stdin.drain()

        line = await asyncio.wait_for(self.process.stdout.readline(), timeout=10.0)
        response = json.loads(line.decode())
        return response

    async def list_tools(self) -> list[dict]:
        """List available tools from the MCP server."""
        try:
            response = await self._send_request("list_tools")
            tools = response.get("result", {}).get("tools", [])
            for t in tools:
                self.tools[t["name"]] = t
            return tools
        except Exception as e:
            logger.warning(f"Failed to list MCP tools: {e}")
            return []

    async def call_tool(self, tool_name: str, arguments: dict | None = None) -> Any:
        """Call a tool on the MCP server."""
        try:
            response = await self._send_request("call_tool", {
                "name": tool_name,
                "arguments": arguments or {},
            })
            result = response.get("result", {})
            content = result.get("content", [])
            return content
        except Exception as e:
            logger.error(f"MCP tool call failed: {e}")
            return f"MCP tool error: {e}"

    def convert_to_langchain_tools(self) -> list:
        """Convert MCP tools to LangChain-compatible tools.

        This creates dynamic @tool-decorated functions for each MCP tool.
        """
        lc_tools = []
        for name, tool_info in self.tools.items():
            input_schema = tool_info.get("inputSchema", {})

            # 从 MCP inputSchema 构造 Pydantic 模型，确保参数正确拆包
            model = self._build_args_model(name, input_schema)

            lc_tool = StructuredTool.from_function(
                name=name,
                description=tool_info.get("description", ""),
                args_schema=model,
                coroutine=self._make_runner(name),
            )
            lc_tools.append(lc_tool)

        return lc_tools

    def _build_args_model(
        self, name: str, schema: dict
    ) -> type[BaseModel] | None:
        """将 MCP inputSchema 转换为 Pydantic 参数模型。"""
        from pydantic import Field, create_model

        properties = schema.get("properties")
        if not properties:
            return None

        type_map = {"string": str, "integer": int, "number": float, "boolean": bool}
        fields = {}
        for prop, info in properties.items():
            py_type = type_map.get(info.get("type", "string"), str)
            fields[prop] = (py_type, Field(description=info.get("description", "")))
        return create_model(f"{name}_schema", **fields)

    def _make_runner(self, name: str):
        """捕获 name 的快照作为默认参数，规避 late-binding closure 问题。"""

        async def runner(**kwargs) -> str:
            result = await self.call_tool(name, kwargs)
            return str(result)

        return runner

    async def close(self):
        """Close the MCP connection."""
        if self.process:
            terminate_result = self.process.terminate()
            if inspect.isawaitable(terminate_result):
                await terminate_result
            await self.process.wait()
            self.process = None


async def load_mcp_tools(server_configs: dict | None) -> list:
    """Explicitly load MCP tools from configured stdio servers.

    Tools are namespaced as mcp:<server>:<tool> to avoid collisions with local tools.
    MCP is opt-in; an empty config returns no tools and performs no subprocess work.
    """
    if not server_configs:
        return []

    loaded = []
    for server_name, config in server_configs.items():
        command = config.get("command") if isinstance(config, dict) else None
        if not command:
            logger.warning("Skipping MCP server %s without command", server_name)
            continue
        args = config.get("args", []) or []
        client = MCPClient()
        try:
            await client.connect_stdio(command, args)
            await client.list_tools()
            for tool in client.convert_to_langchain_tools():
                tool.name = f"mcp:{server_name}:{tool.name}"
                loaded.append(tool)
        finally:
            await client.close()
    return loaded
