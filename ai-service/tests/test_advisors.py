"""AI 推理步骤记录和上下文回溯组件的单元测试"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from agent.advisors import LoggerAdvisor, ReReadAdvisor


class TestLoggerAdvisor:
    """LoggerAdvisor 步骤记录功能测试"""

    @pytest.fixture
    def advisor(self):
        return LoggerAdvisor()

    def test_on_step_stores_step(self, advisor):
        """测试 on_step 能存储单步记录"""
        advisor.on_step({"action": "思考", "content": "分析用户问题"})
        assert len(advisor.get_steps()) == 1
        assert advisor.get_steps()[0]["action"] == "思考"

    def test_on_step_multiple(self, advisor):
        """测试多次调用 on_step 按顺序存储"""
        steps_data = [
            {"action": "思考", "content": "第一步"},
            {"action": "工具调用", "tool": "web_search"},
            {"action": "回复", "content": "最终答案"},
        ]
        for s in steps_data:
            advisor.on_step(s)

        assert len(advisor.get_steps()) == 3
        assert advisor.get_steps() == steps_data

    def test_on_step_with_tool_specifics(self, advisor):
        """测试存储包含工具调用细节的步骤"""
        step = {
            "action": "tool_call",
            "tool": "file_operation",
            "args": {"operation": "read", "path": "test.txt"},
            "result": "文件内容",
        }
        advisor.on_step(step)
        stored = advisor.get_steps()[0]
        assert stored["tool"] == "file_operation"
        assert stored["result"] == "文件内容"

    def test_get_steps_returns_copy(self, advisor):
        """测试 get_steps 返回副本，外部修改不影响内部"""
        advisor.on_step({"action": "test"})
        steps = advisor.get_steps()
        steps.clear()
        assert len(advisor.get_steps()) == 1

    def test_clear_removes_all_steps(self, advisor):
        """测试 clear 清空所有记录"""
        advisor.on_step({"action": "思考"})
        advisor.on_step({"action": "工具调用"})
        advisor.clear()
        assert advisor.get_steps() == []

    def test_clear_then_add(self, advisor):
        """测试清空后重新记录正常工作"""
        advisor.on_step({"action": "旧步骤"})
        advisor.clear()
        advisor.on_step({"action": "新步骤"})
        assert len(advisor.get_steps()) == 1
        assert advisor.get_steps()[0]["action"] == "新步骤"

    def test_initial_state_empty(self, advisor):
        """测试初始化时步骤列表为空"""
        assert advisor.get_steps() == []


class TestReReadAdvisor:
    """ReReadAdvisor 上下文回溯功能测试"""

    @pytest.fixture
    def advisor(self):
        return ReReadAdvisor(recent_n=3)

    def test_fewer_messages_returns_all(self, advisor):
        """测试消息数小于 recent_n*2 时全部返回"""
        messages = [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好"},
        ]
        context = advisor.get_recent_context(messages)
        assert context == messages

    def test_exactly_at_boundary(self, advisor):
        """测试消息数刚好等于 recent_n*2 时全部返回"""
        messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": str(i)} for i in range(6)]
        context = advisor.get_recent_context(messages)
        assert len(context) == 6
        assert context == messages

    def test_exceeds_boundary_trims_oldest(self, advisor):
        """测试超过 recent_n*2 时裁剪最早的消息"""
        messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": str(i)} for i in range(10)]
        context = advisor.get_recent_context(messages)
        # recent_n=3 → 最多保留 6 条
        assert len(context) == 6
        # 保留最近 6 条（索引 4-9）
        assert context[0]["content"] == "4"
        assert context[-1]["content"] == "9"

    def test_empty_messages(self, advisor):
        """测试空消息列表返回空列表"""
        assert advisor.get_recent_context([]) == []

    def test_single_message(self, advisor):
        """测试单条消息"""
        messages = [{"role": "user", "content": "hello"}]
        assert advisor.get_recent_context(messages) == messages

    def test_custom_recent_n(self):
        """测试自定义 recent_n 参数"""
        advisor = ReReadAdvisor(recent_n=5)
        messages = [{"role": "user", "content": str(i)} for i in range(20)]
        context = advisor.get_recent_context(messages)
        # recent_n=5 → 最多保留 10 条
        assert len(context) == 10
        # 保留最近 10 条（索引 10-19）
        assert context[0]["content"] == "10"

    def test_large_recent_n(self):
        """测试 recent_n 大于实际消息数"""
        advisor = ReReadAdvisor(recent_n=100)
        messages = [{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}]
        context = advisor.get_recent_context(messages)
        assert context == messages

    def test_preserves_message_order(self, advisor):
        """测试返回的消息顺序保持不变"""
        messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": str(i)} for i in range(20)]
        context = advisor.get_recent_context(messages)
        # 验证顺序：索引从 14 开始的后续 6 条
        expected = messages[-6:]
        assert context == expected

    def test_different_message_formats(self, advisor):
        """测试不同格式的消息都能正确处理"""
        messages = [
            {"role": "user", "content": "plain text"},
            {"role": "assistant", "content": "", "tool_calls": [{"name": "search"}]},
            {"role": "tool", "content": "result", "tool_call_id": "call_1"},
        ]
        context = advisor.get_recent_context(messages)
        assert len(context) == 3
        # 保留所有消息，包括含额外字段的
        assert "tool_calls" in context[1]
        assert "tool_call_id" in context[2]
