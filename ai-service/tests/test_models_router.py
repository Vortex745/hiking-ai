"""模型列表 API 端点的单元测试"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
import httpx
from unittest.mock import AsyncMock, patch

from httpx import Response, HTTPStatusError, RequestError
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from api.models_router import models_router
from api.models import ModelsFetchRequest, ModelsFetchResponse


# ── 使用 TestClient 的集成测试 ──


@pytest.fixture
def app():
    """创建一个只包含 models_router 的测试应用"""
    app = FastAPI()
    app.include_router(models_router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestModelsFetchEndpoint:
    """models_fetch API 端点功能测试"""

    def test_successful_fetch(self, client):
        """测试成功获取模型列表"""
        async def mock_get(url, headers=None, **kwargs):
            return Response(200, json={
                "data": [
                    {"id": "gpt-4", "object": "model"},
                    {"id": "gpt-3.5-turbo", "object": "model"},
                ]
            })

        with patch("httpx.AsyncClient.get", new=AsyncMock(side_effect=mock_get)):
            response = client.post("/models/fetch", json={
                "base_url": "https://api.openai.com",
                "api_key": "sk-test-key",
            })

        assert response.status_code == 200
        data = response.json()
        assert data["models"] == ["gpt-3.5-turbo", "gpt-4"]  # sorted

    def test_empty_models(self, client):
        """测试 API 返回空模型列表"""
        async def mock_get(url, headers=None, **kwargs):
            return Response(200, json={"data": []})

        with patch("httpx.AsyncClient.get", new=AsyncMock(side_effect=mock_get)):
            response = client.post("/models/fetch", json={
                "base_url": "https://api.openai.com",
                "api_key": "sk-test-key",
            })

        assert response.status_code == 200
        assert response.json()["models"] == []

    def test_http_error(self, client):
        """测试上游 API 返回 HTTP 错误时抛出 HTTPException"""
        async def mock_get(url, headers=None, **kwargs):
            resp = Response(401, request=httpx.Request("GET", url))
            raise HTTPStatusError("401 Unauthorized", request=resp.request, response=resp)

        with patch("httpx.AsyncClient.get", new=AsyncMock(side_effect=mock_get)):
            response = client.post("/models/fetch", json={
                "base_url": "https://api.openai.com",
                "api_key": "sk-invalid",
            })

        assert response.status_code == 401

    def test_connection_error(self, client):
        """测试无法连接到 API 服务器时返回 502"""
        async def mock_get(url, headers=None, **kwargs):
            raise RequestError("Connection refused")

        with patch("httpx.AsyncClient.get", new=AsyncMock(side_effect=mock_get)):
            response = client.post("/models/fetch", json={
                "base_url": "https://invalid-url.example.com",
                "api_key": "sk-test",
            })

        assert response.status_code == 502

    def test_trailing_slash_handling(self, client):
        """测试 base_url 尾部斜杠被 rstrip 正确处理"""
        captured_url = []

        async def mock_get(url, headers=None, **kwargs):
            captured_url.append(url)
            return Response(200, json={"data": [{"id": "gpt-4"}]})

        with patch("httpx.AsyncClient.get", new=AsyncMock(side_effect=mock_get)):
            client.post("/models/fetch", json={
                "base_url": "https://api.openai.com/",
                "api_key": "sk-test",
            })

        assert len(captured_url) == 1
        # base_url 尾部斜杠被去除后拼接 /models
        assert captured_url[0] == "https://api.openai.com/models"

    def test_api_key_in_header(self, client):
        """测试 API Key 正确设置在 Authorization 头中"""
        captured_headers = {}

        async def mock_get(url, headers=None, **kwargs):
            captured_headers.update(headers or {})
            return Response(200, json={"data": [{"id": "gpt-4"}]})

        with patch("httpx.AsyncClient.get", new=AsyncMock(side_effect=mock_get)):
            client.post("/models/fetch", json={
                "base_url": "https://api.openai.com",
                "api_key": "sk-secret-456",
            })

        assert captured_headers.get("Authorization") == "Bearer sk-secret-456"

    def test_malformed_response_data(self, client):
        """测试上游返回格式异常的数据时只返回有效 id"""
        async def mock_get(url, headers=None, **kwargs):
            return Response(200, json={
                "data": [
                    {"id": "gpt-4"},
                    {"id": ""},          # 空 id 应被过滤
                    {"foo": "bar"},       # 无 id 字段
                    "not a dict",         # 非字典
                    None,                 # None
                ]
            })

        with patch("httpx.AsyncClient.get", new=AsyncMock(side_effect=mock_get)):
            response = client.post("/models/fetch", json={
                "base_url": "https://api.openai.com",
                "api_key": "sk-test",
            })

        assert response.status_code == 200
        assert response.json()["models"] == ["gpt-4"]


class TestModelsFetchRequestModel:
    """ModelsFetchRequest Pydantic 模型验证测试"""

    def test_valid_request(self):
        """测试有效请求的模型验证"""
        req = ModelsFetchRequest(base_url="https://api.openai.com", api_key="sk-key")
        assert req.base_url == "https://api.openai.com"
        assert req.api_key == "sk-key"

    def test_missing_base_url(self):
        """测试缺少 base_url 时触发验证错误"""
        with pytest.raises(ValueError):
            ModelsFetchRequest(api_key="sk-key")

    def test_missing_api_key(self):
        """测试缺少 api_key 时触发验证错误"""
        with pytest.raises(ValueError):
            ModelsFetchRequest(base_url="https://api.openai.com")


class TestModelsFetchResponseModel:
    """ModelsFetchResponse Pydantic 模型验证测试"""

    def test_valid_response(self):
        """测试有效响应的模型验证"""
        resp = ModelsFetchResponse(models=["gpt-4", "gpt-3.5"])
        assert resp.models == ["gpt-4", "gpt-3.5"]

    def test_empty_models_list(self):
        """测试空模型列表"""
        resp = ModelsFetchResponse(models=[])
        assert resp.models == []
