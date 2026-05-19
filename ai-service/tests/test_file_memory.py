"""FileChatMemory 持久化存储的单元测试"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import pytest
from unittest.mock import patch

from memory.file_memory import FileChatMemory


@pytest.fixture
def memory(tmp_path):
    """使用临时目录创建 FileChatMemory 实例"""
    save_dir = tmp_path / "chat_data"
    return FileChatMemory("test_chat", save_dir=str(save_dir)), save_dir


class TestFileChatMemory:
    """FileChatMemory 核心功能测试"""

    def test_init_creates_directory(self, tmp_path):
        """测试初始化时自动创建数据目录"""
        save_dir = tmp_path / "new_chat"
        mem = FileChatMemory("chat_1", save_dir=str(save_dir))
        assert save_dir.exists()
        assert save_dir.is_dir()

    def test_add_and_get_messages(self, memory):
        """测试添加消息后能正确获取"""
        mem, _ = memory
        mem.add_message("user", "你好")
        mem.add_message("assistant", "你好！有什么可以帮助你的？")

        messages = mem.get_messages()
        assert len(messages) == 2
        assert messages[0] == {"role": "user", "content": "你好"}
        assert messages[1] == {"role": "assistant", "content": "你好！有什么可以帮助你的？"}

    def test_clear_removes_all_messages(self, memory):
        """测试 clear 后消息列表为空"""
        mem, _ = memory
        mem.add_message("user", "hello")
        mem.add_message("assistant", "world")
        mem.clear()

        assert mem.get_messages() == []

    def test_get_messages_returns_copy(self, memory):
        """测试 get_messages 返回列表副本，修改不影响内部状态"""
        mem, _ = memory
        mem.add_message("user", "test")
        msgs = mem.get_messages()
        msgs.append({"role": "assistant", "content": "hacked"})

        assert len(mem.get_messages()) == 1  # 内部未受影响

    def test_sliding_window_trims_old_messages(self, tmp_path):
        """测试超过 MAX_CONTEXT 的历史消息被自动裁剪"""
        save_dir = tmp_path / "sliding"
        mem = FileChatMemory("sliding_test", save_dir=str(save_dir))
        # MAX_CONTEXT = 30 → 最多保留 60 条消息（30 轮对话）
        max_messages = 60
        # 添加 70 条消息 → 超出上限
        for i in range(70):
            role = "user" if i % 2 == 0 else "assistant"
            mem.add_message(role, f"message_{i}")

        messages = mem.get_messages()
        assert len(messages) == max_messages
        # 验证裁剪后保留的是最新的消息
        assert messages[0]["content"] == "message_10"
        assert messages[-1]["content"] == "message_69"

    def test_sliding_window_boundary(self, tmp_path):
        """测试刚好在窗口边界内不会被裁剪"""
        save_dir = tmp_path / "boundary"
        mem = FileChatMemory("boundary_test", save_dir=str(save_dir))
        # 添加正好 60 条消息（MAX_CONTEXT=30 → 30*2=60）
        for i in range(60):
            role = "user" if i % 2 == 0 else "assistant"
            mem.add_message(role, f"msg_{i}")

        assert len(mem.get_messages()) == 60

    # ── 持久化测试 ──

    def test_persistence_saves_to_disk(self, memory):
        """测试消息被持久化到磁盘文件"""
        mem, save_dir = memory
        mem.add_message("user", "持久化测试")

        json_path = save_dir / "messages.json"
        assert json_path.exists()
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["content"] == "持久化测试"

    def test_persistence_loads_from_disk(self, tmp_path):
        """测试新实例能从磁盘加载先前保存的消息"""
        save_dir = tmp_path / "persist"
        # 第一个实例写入数据
        mem1 = FileChatMemory("p_chat", save_dir=str(save_dir))
        mem1.add_message("user", "保存这条消息")

        # 第二个实例应自动加载
        mem2 = FileChatMemory("p_chat", save_dir=str(save_dir))
        messages = mem2.get_messages()
        assert len(messages) == 1
        assert messages[0]["content"] == "保存这条消息"

    def test_empty_disk_file_returns_empty_list(self, tmp_path):
        """测试磁盘文件为空时初始化空的会话"""
        save_dir = tmp_path / "empty"
        save_dir.mkdir(parents=True, exist_ok=True)
        # 创建空文件
        (save_dir / "messages.json").write_text("[]", encoding="utf-8")

        mem = FileChatMemory("empty_chat", save_dir=str(save_dir))
        assert mem.get_messages() == []

    def test_corrupted_disk_file_handling(self, tmp_path):
        """测试磁盘文件损坏时优雅处理"""
        save_dir = tmp_path / "corrupted"
        save_dir.mkdir(parents=True, exist_ok=True)
        (save_dir / "messages.json").write_text("{invalid json}", encoding="utf-8")

        mem = FileChatMemory("corrupted_chat", save_dir=str(save_dir))
        # 文件损坏时应返回空列表而不是崩溃
        assert mem.get_messages() == []

    # ── 多会话隔离 ──

    def test_multiple_sessions_isolated(self, tmp_path):
        """测试不同 chat_id 的消息互不干扰"""
        base_dir = tmp_path / "multi"
        mem_a = FileChatMemory("chat_a", save_dir=str(base_dir / "chat_a"))
        mem_b = FileChatMemory("chat_b", save_dir=str(base_dir / "chat_b"))

        mem_a.add_message("user", "这是 A 的消息")
        mem_b.add_message("user", "这是 B 的消息")

        assert len(mem_a.get_messages()) == 1
        assert mem_a.get_messages()[0]["content"] == "这是 A 的消息"
        assert mem_b.get_messages()[0]["content"] == "这是 B 的消息"
