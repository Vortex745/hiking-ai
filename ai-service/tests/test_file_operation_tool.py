import importlib

import pytest


@pytest.mark.asyncio
async def test_file_operation_rejects_sibling_workspace_escape(monkeypatch, tmp_path):
    file_operation_module = importlib.import_module("tools.file_operation")
    from tools.file_operation import file_operation

    workspace = tmp_path / "workspace"
    sibling_target = tmp_path / "workspace_evil" / "pwned.txt"
    monkeypatch.setattr(file_operation_module, "WORKSPACE_DIR", workspace)

    result = await file_operation.ainvoke({
        "operation": "write",
        "path": "../workspace_evil/pwned.txt",
        "content": "pwned",
    })

    assert "超出" in result
    assert not sibling_target.exists()


@pytest.mark.asyncio
async def test_resource_download_rejects_sibling_workspace_escape(monkeypatch, tmp_path):
    resource_download_module = importlib.import_module("tools.resource_download")
    from tools.resource_download import resource_download

    class FakeResponse:
        content = b"pwned"

        def raise_for_status(self):
            return None

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def get(self, url):
            return FakeResponse()

    workspace = tmp_path / "workspace"
    sibling_target = tmp_path / "workspace_evil" / "pwned.txt"
    monkeypatch.setattr(resource_download_module, "WORKSPACE_DIR", workspace)
    monkeypatch.setattr(resource_download_module.httpx, "AsyncClient", FakeAsyncClient)

    result = await resource_download.ainvoke({
        "url": "https://example.com/pwned.txt",
        "save_path": "../workspace_evil/pwned.txt",
    })

    assert "超出" in result
    assert not sibling_target.exists()
