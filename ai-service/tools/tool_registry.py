"""工具注册表模块。

提供工具元数据管理、风险分级、速率限制和调用前验证。
是 AVAILABLE_TOOLS 的替代方案，将所有工具元数据集中管理。
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from tools.risk_classifier import RiskLevel, classify_tool, requires_confirmation


@dataclass
class ToolValidationResult:
    """工具调用验证结果。"""

    valid: bool
    error: str | None = None


@dataclass
class ToolCallRequest:
    """工具调用请求的完整表示。

    包含风险分类和速率限制信息，供 callbacks 和 confirmation 端点使用。
    """

    name: str
    args: dict[str, Any]
    risk_level: RiskLevel
    needs_confirmation: bool
    rate_limit_remaining: int | None = None

    @property
    def requires_confirmation(self) -> bool:
        """Backward-compatible alias for older callers."""
        return self.needs_confirmation


@dataclass
class ToolMetadata:
    """工具的完整元数据定义。"""

    name: str
    description: str
    parameters: dict[str, Any]
    risk_level: RiskLevel | None = None  # None 表示自动从 TOOL_RISK_MAP 推断
    rate_limit_per_minute: int = 30  # 每分钟允许的最大调用次数
    requires_confirmation: bool | None = None  # 旧字段名，保留兼容
    needs_confirmation: bool | None = None  # None 表示按 risk_level 自动判定
    domain: str = "general"
    scenarios: tuple[str, ...] | list[str] = field(default_factory=tuple)
    auto_allowed: bool = True
    result_policy: str = "raw"
    hidden: bool = False

    def __post_init__(self) -> None:
        if self.needs_confirmation is None and self.requires_confirmation is not None:
            self.needs_confirmation = self.requires_confirmation
        elif self.requires_confirmation is None and self.needs_confirmation is not None:
            self.requires_confirmation = self.needs_confirmation

        if not isinstance(self.scenarios, tuple):
            self.scenarios = tuple(self.scenarios)


class TokenBucket:
    """简单的令牌桶速率限制器。"""

    def __init__(self, capacity: int, fill_rate: float) -> None:
        self.capacity = capacity
        self.fill_rate = fill_rate  # 每秒补充的令牌数
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)
        self.last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        """尝试消耗 tokens 个令牌。有足够令牌时返回 True，否则 False。"""
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    @property
    def remaining(self) -> int:
        """当前剩余令牌数（向下取整）。"""
        self._refill()
        return int(self.tokens)


class ToolRegistry:
    """工具注册表。

    集中管理所有工具的元数据、风险分类和速率限制。
    取代原先散布在 agent/system_prompt 中的静态工具列表。
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolMetadata] = {}
        self._buckets: dict[str, TokenBucket] = {}

    # ── 注册 ──────────────────────────────────────────────

    def register(self, metadata: ToolMetadata) -> None:
        """注册一个工具。"""
        name = metadata.name
        if name in self._tools:
            raise ValueError(f'工具 "{name}" 已注册')
        self._tools[name] = metadata
        # 按 rate_limit_per_minute 创建令牌桶（capacity = rate, fill = rate/60）
        rate = metadata.rate_limit_per_minute
        self._buckets[name] = TokenBucket(capacity=rate, fill_rate=rate / 60.0)

    def register_many(self, metadata_list: list[ToolMetadata]) -> None:
        """批量注册工具。"""
        for md in metadata_list:
            self.register(md)

    # ── 读取 ──────────────────────────────────────────────

    def get(self, name: str) -> ToolMetadata | None:
        """按名称获取工具元数据，不存在时返回 None。"""
        return self._tools.get(name)

    def list_tools(self, include_hidden: bool = False) -> list[ToolMetadata]:
        """返回已注册工具列表。

        默认只返回基础可见工具，保持现有 API 行为；领域工具可通过
        include_hidden=True 或 get(name) 访问。
        """
        if include_hidden:
            return list(self._tools.values())
        return [md for md in self._tools.values() if not md.hidden]

    def list_all_tools(self) -> list[ToolMetadata]:
        """返回所有工具，包含按场景动态暴露的领域工具。"""
        return self.list_tools(include_hidden=True)

    def __contains__(self, name: str) -> bool:
        return name in self._tools

    def __len__(self) -> int:
        return len(self.list_tools())

    # ── 验证 ──────────────────────────────────────────────

    def validate_call(self, name: str, args: dict[str, Any]) -> ToolValidationResult:
        """验证工具调用请求。

        检查：
          1. 工具是否已注册。
          2. 是否超出速率限制。

        Args:
            name: 工具名称。
            args: 调用参数（当前仅做格式检查，可通过自定义 validator 扩展）。

        Returns:
            ToolValidationResult，包含验证通过/失败状态和错误信息。
        """
        md = self._tools.get(name)
        if md is None:
            return ToolValidationResult(valid=False, error=f'未知工具: "{name}"')

        # 检查速率限制
        bucket = self._buckets.get(name)
        if bucket is not None and not bucket.consume():
            remaining_sec = int(
                60.0 / md.rate_limit_per_minute if md.rate_limit_per_minute > 0 else 60
            )
            return ToolValidationResult(
                valid=False,
                error=f'工具 "{name}" 已达到速率限制，请 {max(remaining_sec, 1)} 秒后重试',
            )

        # 检查参数类型（确保是 dict）
        if not isinstance(args, dict):
            return ToolValidationResult(valid=False, error="参数必须是 JSON 对象（dict）")

        return ToolValidationResult(valid=True)

    # ── 风险 & 确认 ──────────────────────────────────────

    def get_risk_level(self, name: str) -> RiskLevel:
        """获取工具的风险级别。"""
        md = self._tools.get(name)
        if md is None:
            return RiskLevel.MEDIUM
        if md.risk_level is not None:
            return md.risk_level
        return classify_tool(name)

    def needs_confirmation(self, name: str) -> bool:
        """判断工具调用是否需要用户确认。

        优先使用 metadata.requires_confirmation 的显式设置，
        否则按风险级别自动推断。
        """
        md = self._tools.get(name)
        if md is None:
            return False
        if md.needs_confirmation is not None:
            return md.needs_confirmation
        if md.requires_confirmation is not None:
            return md.requires_confirmation
        return requires_confirmation(self.get_risk_level(name))

    def get_call_request(self, name: str, args: dict[str, Any]) -> ToolCallRequest | None:
        """构建一个完整的 ToolCallRequest（含风险 & 速率信息）。

        当工具不存在时返回 None。
        """
        md = self._tools.get(name)
        if md is None:
            return None

        bucket = self._buckets.get(name)
        remaining = bucket.remaining if bucket else None

        return ToolCallRequest(
            name=name,
            args=args,
            risk_level=self.get_risk_level(name),
            needs_confirmation=self.needs_confirmation(name),
            rate_limit_remaining=remaining,
        )

    # ── 工具列表（给前端的 API） ─────────────────────────

    def tools_api_response(self, include_hidden: bool = False) -> list[dict[str, Any]]:
        """生成符合前端 /api/tools 接口要求的响应格式。

        前端期望的格式：
          [{
            "function": {
              "name": "...",
              "description": "...",
              "parameters": {...}
            }
          }]
        """
        result = []
        for md in self.list_tools(include_hidden=include_hidden):
            result.append(
                {
                    "function": {
                        "name": md.name,
                        "description": md.description,
                        "parameters": md.parameters,
                        "domain": md.domain,
                        "scenarios": list(md.scenarios),
                        "auto_allowed": md.auto_allowed,
                        "risk_level": self.get_risk_level(md.name).value,
                        "needs_confirmation": self.needs_confirmation(md.name),
                        "result_policy": md.result_policy,
                        "hidden": md.hidden,
                    }
                }
            )
        return result
