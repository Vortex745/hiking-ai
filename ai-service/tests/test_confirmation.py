"""测试确认流程：ConfirmationStore + /chat/confirm 端点 + SSE 拦截。"""

import time
import uuid

import pytest
from fastapi.testclient import TestClient

from api.confirmation_store import ConfirmationStore, get_store, PendingConfirmation
from api.models import ConfirmRequest, ConfirmResponse, PendingConfirmationsResponse


# ── ConfirmationStore 单元测试 ─────────────────────────────


class TestConfirmationStore:
    def test_add_and_get(self):
        store = ConfirmationStore()
        cid = store.add("delete_file", {"path": "/tmp/x"}, chat_id="chat-1", step=0)
        rec = store.get(cid)
        assert rec is not None
        assert rec.tool_name == "delete_file"
        assert rec.args == {"path": "/tmp/x"}
        assert rec.chat_id == "chat-1"
        assert rec.step == 0
        assert rec.status == "pending"

    def test_add_with_custom_id(self):
        store = ConfirmationStore()
        cid = "my-custom-id"
        returned = store.add(
            "send_email", {"to": "a@b.com"}, chat_id="chat-1", step=0, confirmation_id=cid
        )
        assert returned == cid
        rec = store.get(cid)
        assert rec is not None
        assert rec.confirmation_id == cid

    def test_get_nonexistent(self):
        store = ConfirmationStore()
        assert store.get("does-not-exist") is None

    def test_confirm(self):
        store = ConfirmationStore()
        cid = store.add("delete_file", {}, chat_id="chat-1", step=0)
        assert store.confirm(cid) is True
        assert store.get(cid).status == "confirmed"

    def test_confirm_twice_returns_false(self):
        store = ConfirmationStore()
        cid = store.add("delete_file", {}, chat_id="chat-1", step=0)
        assert store.confirm(cid) is True
        assert store.confirm(cid) is False  # 第二次返回 False

    def test_reject(self):
        store = ConfirmationStore()
        cid = store.add("delete_file", {}, chat_id="chat-1", step=0)
        assert store.reject(cid) is True
        assert store.get(cid).status == "rejected"

    def test_confirm_rejected_returns_false(self):
        store = ConfirmationStore()
        cid = store.add("delete_file", {}, chat_id="chat-1", step=0)
        assert store.reject(cid) is True
        assert store.confirm(cid) is False  # 已被拒绝，不能确认
        assert store.get(cid).status == "rejected"

    def test_get_pending_by_chat(self):
        store = ConfirmationStore()
        c1 = store.add("tool1", {}, chat_id="chat-1", step=0)
        c2 = store.add("tool2", {}, chat_id="chat-1", step=1)
        c3 = store.add("tool3", {}, chat_id="chat-2", step=0)

        pending = store.get_pending_by_chat("chat-1")
        ids = {r.confirmation_id for r in pending}
        assert c1 in ids
        assert c2 in ids
        assert c3 not in ids

    def test_get_pending_excludes_confirmed(self):
        store = ConfirmationStore()
        cid = store.add("tool1", {}, chat_id="chat-1", step=0)
        store.confirm(cid)
        pending = store.get_pending_by_chat("chat-1")
        assert len(pending) == 0

    def test_cleanup_expired(self):
        store = ConfirmationStore()
        c1 = store.add("tool1", {}, chat_id="chat-1", step=0)
        # 手动把 created_at 设置为过去
        rec = store.get(c1)
        rec.created_at = time.time() - 100  # 100 秒前
        c2 = store.add("tool2", {}, chat_id="chat-1", step=1)  # 当前时间

        cleaned = store.cleanup_expired(max_age=50)
        assert cleaned == 1
        assert store.get(c1) is None
        assert store.get(c2) is not None

    def test_get_store_singleton(self):
        s1 = get_store()
        s2 = get_store()
        assert s1 is s2


# ── HTTP 端点测试 ──────────────────────────────────────────


@pytest.fixture
def client():
    """重置商店并返回 TestClient。"""
    from main import app

    # 重置确认存储以避免跨测试污染
    import api.confirmation_store as cs

    cs._store = ConfirmationStore()

    with TestClient(app) as c:
        yield c


class TestConfirmHttpEndpoint:
    def test_confirm_valid(self, client):
        store = get_store()
        cid = store.add("danger_tool", {"key": "val"}, chat_id="chat-1", step=0)

        resp = client.post("/api/v1/chat/confirm", json={
            "confirmation_id": cid,
            "action": "confirm",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "confirmed"
        assert data["confirmation_id"] == cid
        assert store.get(cid).status == "confirmed"

    def test_reject_valid(self, client):
        store = get_store()
        cid = store.add("danger_tool", {"key": "val"}, chat_id="chat-1", step=0)

        resp = client.post("/api/v1/chat/confirm", json={
            "confirmation_id": cid,
            "action": "reject",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "confirmed"
        assert data["confirmation_id"] == cid
        assert store.get(cid).status == "confirmed"

    def test_reject_valid(self, client):
        store = get_store()
        cid = store.add("danger_tool", {}, chat_id="chat-1", step=0)

        resp = client.post("/api/v1/chat/confirm", json={
            "confirmation_id": cid,
            "action": "reject",
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "rejected"
        assert store.get(cid).status == "rejected"

    def test_confirm_not_found(self, client):
        resp = client.post("/api/v1/chat/confirm", json={
            "confirmation_id": "does-not-exist",
            "action": "confirm",
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "not_found"

    def test_confirm_already_resolved(self, client):
        store = get_store()
        cid = store.add("danger_tool", {}, chat_id="chat-1", step=0)
        store.confirm(cid)

        resp = client.post("/api/v1/chat/confirm", json={
            "confirmation_id": cid,
            "action": "reject",
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "already_resolved"

    def test_confirm_invalid_action(self, client):
        resp = client.post("/api/v1/chat/confirm", json={
            "confirmation_id": "any",
            "action": "maybe",
        })
        assert resp.status_code == 400

    def test_get_pending(self, client):
        store = get_store()
        store.add("tool1", {"a": 1}, chat_id="chat-1", step=0)
        store.add("tool2", {"b": 2}, chat_id="chat-1", step=1)
        store.add("tool3", {"c": 3}, chat_id="chat-2", step=0)

        resp = client.get("/api/v1/chat/pending/chat-1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["chat_id"] == "chat-1"
        assert len(data["pending"]) == 2

    def test_get_pending_empty(self, client):
        resp = client.get("/api/v1/chat/pending/empty-chat")
        assert resp.status_code == 200
        assert resp.json()["pending"] == []


# ── SSE 拦截逻辑测试 ──────────────────────────────────────


def test_tool_call_interception_adds_confirmation_id():
    """验证 needs_confirm=True 的 tool_call 事件被注入 confirmation_id。"""
    store = get_store()
    # 重置
    import api.confirmation_store as cs
    cs._store = ConfirmationStore()
    store = get_store()

    # 模拟一次 tool_call 事件的拦截
    tool_event = {
        "type": "tool_call",
        "content": "delete_file",
        "metadata": {
            "risk_level": "high",
            "needs_confirm": True,
            "rate_limited": False,
            "args": {"path": "/tmp/x"},
        },
    }

    metadata = tool_event.get("metadata")
    if isinstance(metadata, dict) and metadata.get("needs_confirm", False):
        cid = store.add(
            tool_name=tool_event.get("content", ""),
            args=metadata.get("args", {}),
            chat_id="test-chat",
            step=0,
        )
        metadata["confirmation_id"] = cid

    assert "confirmation_id" in tool_event["metadata"]
    rec = store.get(tool_event["metadata"]["confirmation_id"])
    assert rec is not None
    assert rec.tool_name == "delete_file"
    assert rec.status == "pending"


def test_tool_call_without_needs_confirm_not_stored():
    """验证不需要确认的 tool_call 不会被拦截。"""
    store = get_store()
    import api.confirmation_store as cs
    cs._store = ConfirmationStore()
    store = get_store()

    tool_event = {
        "type": "tool_call",
        "content": "get_weather",
        "metadata": {
            "risk_level": "low",
            "needs_confirm": False,
            "rate_limited": False,
        },
    }

    metadata = tool_event.get("metadata")
    if isinstance(metadata, dict) and metadata.get("needs_confirm", False):
        cid = store.add(
            tool_name=tool_event.get("content", ""),
            args=metadata.get("args", {}),
            chat_id="test-chat",
            step=0,
        )
        metadata["confirmation_id"] = cid

    assert "confirmation_id" not in tool_event.get("metadata", {})
    assert len(store.get_pending_by_chat("test-chat")) == 0
