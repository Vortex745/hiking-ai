from __future__ import annotations

import asyncio
import json

from fastapi.testclient import TestClient

from main import app


def test_artifact_download_serves_workspace_file(monkeypatch, tmp_path):
    from api import artifacts as artifacts_api

    monkeypatch.setattr(artifacts_api, "WORKSPACE_DIR", tmp_path)
    pdf_path = tmp_path / "trip.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 demo")

    client = TestClient(app)
    response = client.get("/api/v1/artifacts/trip.pdf")

    assert response.status_code == 200
    assert response.content == b"%PDF-1.4 demo"
    assert response.headers["content-type"] == "application/pdf"


def test_artifact_download_rejects_missing_file(monkeypatch, tmp_path):
    from api import artifacts as artifacts_api

    monkeypatch.setattr(artifacts_api, "WORKSPACE_DIR", tmp_path)

    client = TestClient(app)
    response = client.get("/api/v1/artifacts/missing.pdf")

    assert response.status_code == 404


def test_generate_pdf_returns_download_metadata(monkeypatch, tmp_path):
    from tools import pdf_generation

    monkeypatch.setattr(pdf_generation, "WORKSPACE_DIR", tmp_path)

    result = asyncio.run(
        pdf_generation.generate_pdf.ainvoke({
            "title": "Baiyun hike guide",
            "content": "Route: south gate to summit.",
        })
    )

    artifact = result["artifact"]
    serialized = json.dumps(result, ensure_ascii=False)

    assert result["ok"] is True
    assert artifact["kind"] == "pdf"
    assert artifact["filename"].endswith(".pdf")
    assert artifact["download_url"].startswith("/api/v1/artifacts/")
    assert artifact["mime_type"] == "application/pdf"
    assert "C:\\" not in serialized
    assert "/tmp/" not in serialized


def test_trip_report_export_exposes_pdf_artifact_without_absolute_path(monkeypatch, tmp_path):
    from tools import hiking_domain, pdf_generation

    monkeypatch.setattr(hiking_domain, "WORKSPACE_DIR", tmp_path)
    monkeypatch.setattr(pdf_generation, "WORKSPACE_DIR", tmp_path)

    result = asyncio.run(
        hiking_domain.trip_report_export.ainvoke({
            "title": "Weekend hike plan",
            "content": "Day one follows a mature trail. Day two stays short.",
            "format": "pdf",
        })
    )

    serialized = json.dumps(result, ensure_ascii=False)
    pdf_artifact = next(item for item in result["artifacts"] if item["kind"] == "pdf")

    assert result["ok"] is True
    assert pdf_artifact["download_url"].startswith("/api/v1/artifacts/")
    assert "markdown_path" not in result
    assert "C:\\" not in serialized
    assert "/tmp/" not in serialized
