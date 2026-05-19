from api.chat import _attach_confirmation_if_needed
from api.confirmation_store import ConfirmationStore


def test_confirmation_uses_needs_confirmation_metadata_key():
    store = ConfirmationStore()
    event = {
        "type": "tool_call",
        "content": "第 1 步：调用 file_operation，参数：{}",
        "metadata": {
            "tool": "file_operation",
            "args": {"operation": "create", "path": "workspace/a.md"},
            "needs_confirmation": True,
        },
    }

    _attach_confirmation_if_needed(event, store=store, chat_id="chat-1", step=3)

    confirmation_id = event["metadata"].get("confirmation_id")
    assert confirmation_id
    record = store.get(confirmation_id)
    assert record is not None
    assert record.tool_name == "file_operation"
    assert record.args == {"operation": "create", "path": "workspace/a.md"}
    assert record.chat_id == "chat-1"
    assert record.step == 3


def test_confirmation_ignores_legacy_needs_confirm_key():
    store = ConfirmationStore()
    event = {
        "type": "tool_call",
        "content": "legacy",
        "metadata": {
            "tool": "file_operation",
            "args": {},
            "needs_confirm": True,
        },
    }

    _attach_confirmation_if_needed(event, store=store, chat_id="chat-1", step=1)

    assert "confirmation_id" not in event["metadata"]
    assert store.get_pending_by_chat("chat-1") == []
