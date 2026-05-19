"""Tests for the Feishu document integration module (lark-cli based)."""

import sys
import os
import json
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ensure OPENAI_API_KEY is set (config.py requires it on import)
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "test-key-for-testing"


from rag.feishu import (
    _run_lark_cli,
    _LARK_CLI_PATH,
    extract_doc_token,
    inspect_feishu_link,
    list_wiki_nodes,
    resolve_wiki_node,
    search_feishu_docs,
    FeishuDocLoader,
    FeishuDefaultSyncer,
)


FEISHU_EXTERNAL_ERROR_MARKERS = (
    "lark-cli 未安装",
    "lark-cli 命令超时",
    "lark-cli API 错误",
    "Permission denied",
    "auth login",
    "99991679",
)


def _skip_if_feishu_external_error(exc: Exception) -> None:
    """Skip live Feishu checks when local lark-cli auth/permission is unavailable."""
    message = str(exc)
    if any(marker in message for marker in FEISHU_EXTERNAL_ERROR_MARKERS):
        pytest.skip(f"Feishu lark-cli unavailable or unauthorized: {message}")


# ── Cycle 1: _run_lark_cli tracer bullet ──────────────────────────

class TestRunLarkCli:
    """Verify the lark-cli subprocess wrapper works end-to-end."""

    def test_calls_lark_cli_and_returns_parsed_json(self):
        """Tracer bullet: a real lark-cli call returns ok=True with data."""
        result = _run_lark_cli(["drive", "+search", "--query", "test", "--page-size", "1"])
        assert result["ok"] is True
        assert "data" in result

    def test_returns_results_with_expected_search_fields(self):
        """Search results contain the fields we depend on."""
        result = _run_lark_cli(["drive", "+search", "--query", "test", "--page-size", "2"])
        data = result["data"]
        assert "results" in data
        assert "has_more" in data
        assert "total" in data
        assert isinstance(data["results"], list)

    def test_raises_on_invalid_command(self):
        """An invalid lark-cli command raises RuntimeError."""
        with pytest.raises(RuntimeError):
            _run_lark_cli(["no_such_command_xyz"])

    def test_lark_cli_resolved_to_full_path(self):
        """_LARK_CLI_PATH should be an absolute path, not just 'lark-cli'."""
        assert os.path.isabs(_LARK_CLI_PATH) or "/" in _LARK_CLI_PATH


# ── Cycle 2: search_feishu_docs ────────────────────────────────────

class TestSearchFeishuDocs:
    """Verify searching Feishu cloud documents via lark-cli."""

    def test_search_with_keyword_returns_results(self):
        """Keyword search returns at least one result."""
        result = search_feishu_docs(query="test", page_size=3)
        assert result["total"] > 0
        assert len(result["results"]) >= 1

    def test_results_contain_document_metadata(self):
        """Each result has token, doc_types, and url."""
        result = search_feishu_docs(query="test", page_size=2)
        for item in result["results"]:
            meta = item["result_meta"]
            assert "token" in meta
            assert "doc_types" in meta
            assert "url" in meta

    def test_pagination_fields_present(self):
        """Response includes has_more and page_token for pagination."""
        result = search_feishu_docs(query="test", page_size=1)
        assert isinstance(result["has_more"], bool)
        assert isinstance(result["page_token"], str)

    def test_empty_query_browses_all_documents(self):
        """Empty query string returns documents without keyword filter."""
        result = search_feishu_docs(query="", page_size=2)
        assert result["total"] > 0
        assert len(result["results"]) >= 1

    def test_page_size_respected(self):
        """Results respect the requested page_size."""
        result = search_feishu_docs(query="test", page_size=2)
        assert len(result["results"]) <= 2

    def test_pagination_advances_with_page_token(self):
        """A second page with page_token returns different results."""
        page1 = search_feishu_docs(query="test", page_size=2)
        if page1["has_more"]:
            page2 = search_feishu_docs(
                query="test", page_size=2, page_token=page1["page_token"]
            )
            # Should have results and a different page token
            assert len(page2["results"]) >= 1
            assert page2["page_token"] != page1["page_token"]
        else:
            pytest.skip("Not enough documents for pagination test")


# ── Cycle 3: FeishuDocLoader ──────────────────────────────────────

class TestFeishuDocLoader:
    """Verify document fetching and chunking via lark-cli."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Find a real document token to test against."""
        search = search_feishu_docs(query="test", page_size=1)
        if not search["results"]:
            pytest.skip("No Feishu documents available for testing")
        self.doc_token = search["results"][0]["result_meta"]["token"]
        self.doc_type = search["results"][0]["result_meta"].get("doc_types", "docx").lower()
        self.loader = FeishuDocLoader()
        try:
            self.loader.fetch_content(self.doc_token, doc_type=self.doc_type)
        except RuntimeError as exc:
            _skip_if_feishu_external_error(exc)
            raise

    def test_fetch_content_returns_markdown_and_title(self):
        """fetch_content returns a dict with markdown, title, and doc_id."""
        fetched = self.loader.fetch_content(self.doc_token)
        assert isinstance(fetched, dict)
        assert "markdown" in fetched
        assert "title" in fetched
        assert "doc_id" in fetched
        assert len(fetched["markdown"]) > 0

    def test_load_and_split_returns_documents_with_metadata(self):
        """load_and_split returns LangChain Documents with correct metadata."""
        docs = self.loader.load_and_split(self.doc_token, doc_type=self.doc_type)
        assert len(docs) > 0
        for doc in docs:
            assert doc.page_content
            assert doc.metadata["source"] == "feishu"
            assert doc.metadata["feishu_doc_token"] == self.doc_token
            assert doc.metadata["feishu_doc_type"] == self.doc_type

    def test_load_and_split_respects_custom_title(self):
        """Custom title overrides the fetched title in metadata."""
        custom_title = "My Custom Document Title"
        docs = self.loader.load_and_split(
            self.doc_token, title=custom_title, doc_type=self.doc_type
        )
        for doc in docs:
            assert doc.metadata["title"] == custom_title

    def test_load_and_split_uses_fetched_title_when_no_custom(self):
        """Without a custom title, the fetched title from Feishu is used."""
        docs = self.loader.load_and_split(self.doc_token, doc_type=self.doc_type)
        fetched = self.loader.fetch_content(self.doc_token)
        expected_title = fetched["title"]
        for doc in docs:
            assert doc.metadata["title"] == expected_title

    def test_chunk_overlap_is_respected(self):
        """Adjacent chunks share overlap text."""
        docs = self.loader.load_and_split(self.doc_token, doc_type=self.doc_type)
        if len(docs) < 2:
            pytest.skip("Document only has one chunk, can't verify overlap")

        # The last N characters of chunk1 should appear at the start of chunk2
        # (RecursiveCharacterTextSplitter with overlap=200)
        overlap_end = docs[0].page_content[-50:]
        assert overlap_end in docs[1].page_content

    def test_fetch_content_returns_clean_text_without_html_tags(self):
        """V2 API fetch_content returns plain text, not raw HTML."""
        fetched = self.loader.fetch_content(self.doc_token)
        content = fetched["markdown"]
        # V2 API returns HTML; our adapter must strip HTML tags
        for tag in ("<h1>", "<h2>", "<table>", "<p>", "<blockquote>"):
            assert tag not in content, f"HTML tag {tag} found in fetched content"
        assert len(content.strip()) > 0


# ── Cycle 3: Feishu URL detection in query ─────────────────────────

def test_detect_feishu_in_question_with_url():
    """extract_doc_token finds Feishu doc tokens inside full question strings."""
    from rag.feishu import extract_doc_token
    question = "请总结 https://xxx.feishu.cn/docx/AbCdEf1234567890abcdef 的内容"
    token = extract_doc_token(question)
    assert token == "AbCdEf1234567890abcdef"

    question2 = "看看这篇 https://xxx.feishu.cn/doc/XyZ0987654321AbCdEfGhIj 说了什么"
    token2 = extract_doc_token(question2)
    assert token2 == "XyZ0987654321AbCdEfGhIj"


def test_detect_feishu_returns_none_for_plain_text():
    """Plain text without Feishu URL returns the original text as-is."""
    from rag.feishu import extract_doc_token
    question = "什么是RAG？它有什么用途？"
    result = extract_doc_token(question)
    assert result == question


def test_fetch_feishu_from_question_url_end_to_end():
    """Full pipeline: question with Feishu URL → fetch doc → return clean content."""
    from rag.feishu import extract_doc_token, FeishuDocLoader

    loader = FeishuDocLoader()
    search = search_feishu_docs(query="test", page_size=1)
    if not search["results"]:
        pytest.skip("No Feishu documents available")
    doc_token = search["results"][0]["result_meta"]["token"]

    # Simulate: user asks a question containing a Feishu URL
    question = f"这篇文章在说什么？https://feishu.cn/docx/{doc_token}"
    extracted = extract_doc_token(question)
    assert extracted == doc_token

    try:
        fetched = loader.fetch_content(extracted)
    except RuntimeError as exc:
        _skip_if_feishu_external_error(exc)
        raise
    assert len(fetched["markdown"]) > 0
    # Content must be clean (no HTML tags from v2 API)
    assert "<h1>" not in fetched["markdown"]


# ── Cycle 1: HTML→text conversion ─────────────────────────────────

def test_html_to_text_strips_tags_and_preserves_content():
    """_html_to_text converts v2 API HTML to readable plain text."""
    from rag.feishu import _html_to_text
    html = "<h1>Test Title</h1><p>Hello <b>World</b></p><ul><li>Item 1</li><li>Item 2</li></ul>"
    text = _html_to_text(html)
    assert "Test Title" in text
    assert "Hello World" in text
    assert "Item 1" in text
    assert "Item 2" in text
    assert "<h1>" not in text
    assert "<p>" not in text
    assert "<b>" not in text


def test_html_to_text_handles_empty_html():
    """_html_to_text handles empty or whitespace-only HTML."""
    from rag.feishu import _html_to_text
    assert _html_to_text("") == ""
    assert _html_to_text("<p></p>").strip() == ""


# ── Cycle 4: extract_doc_token + FeishuDefaultSyncer ──────────────

class TestExtractDocToken:
    """Verify URL-to-token extraction."""

    def test_extracts_token_from_docx_url(self):
        url = "https://xxx.feishu.cn/docx/AbCdEf1234567890abcdef"
        assert extract_doc_token(url) == "AbCdEf1234567890abcdef"

    def test_extracts_token_from_doc_url(self):
        url = "https://xxx.feishu.cn/doc/XyZ0987654321AbCdEfGhIj"
        assert extract_doc_token(url) == "XyZ0987654321AbCdEfGhIj"

    def test_extracts_token_from_bitable_url(self):
        url = "https://xxx.feishu.cn/bitable/BTbL1234567890abcdefgh"
        assert extract_doc_token(url) == "BTbL1234567890abcdefgh"

    def test_extracts_wiki_node_token_from_url(self):
        url = "https://xxx.feishu.cn/wiki/WIKINodeToken1234567890ab"
        assert extract_doc_token(url) == "WIKINodeToken1234567890ab"

    def test_inspects_wiki_link_as_node(self):
        url = "https://xxx.feishu.cn/wiki/WIKINodeToken1234567890ab"
        link = inspect_feishu_link(url)
        assert link.kind == "wiki_node"
        assert link.token == "WIKINodeToken1234567890ab"
        assert link.doc_type == "wiki"

    def test_passes_through_plain_token(self):
        token = "SREndflzEonZnIxyGBEcLtEmnuQ"
        assert extract_doc_token(token) == token

    def test_raises_on_invalid_url(self):
        with pytest.raises(ValueError, match="无法从 URL 中提取文档 token"):
            extract_doc_token("https://example.com/not/a/feishu/url")


def test_resolve_wiki_node_uses_lark_api_get_node(monkeypatch):
    """Wiki node links should be screened through Feishu OpenAPI via lark-cli api."""

    calls = []

    def fake_run(args):
        calls.append(args)
        assert args[0:3] == ["api", "GET", "/open-apis/wiki/v2/spaces/get_node"]
        assert args[3] == "--params"
        assert json.loads(args[4]) == {
            "token": "WIKINodeToken1234567890ab",
            "obj_type": "wiki",
        }
        return {
            "ok": True,
            "data": {
                "node": {
                    "node_token": "WIKINodeToken1234567890ab",
                    "obj_token": "DOCXToken1234567890abcdef",
                    "obj_type": "docx",
                    "title": "Wiki 页面",
                    "space_id": "1234567890",
                }
            },
        }

    monkeypatch.setattr("rag.feishu._run_lark_cli", fake_run)

    node = resolve_wiki_node("WIKINodeToken1234567890ab")

    assert node["obj_token"] == "DOCXToken1234567890abcdef"
    assert node["obj_type"] == "docx"
    assert node["title"] == "Wiki 页面"
    assert calls


def test_list_wiki_nodes_uses_lark_api_space_nodes_endpoint(monkeypatch):
    """Wiki space traversal should call the documented OpenAPI nodes endpoint."""

    calls = []

    def fake_run(args):
        calls.append(args)
        assert args[0:3] == ["api", "GET", "/open-apis/wiki/v2/spaces/space123/nodes"]
        assert args[3] == "--params"
        assert json.loads(args[4]) == {
            "page_size": 20,
            "parent_node_token": "parent123",
        }
        return {
            "ok": True,
            "data": {
                "items": [{"node_token": "node1", "title": "Wiki 页面"}],
                "has_more": False,
                "page_token": "",
            },
        }

    monkeypatch.setattr("rag.feishu._run_lark_cli", fake_run)

    page = list_wiki_nodes("space123", parent_node_token="parent123", page_size=20)

    assert page["items"][0]["node_token"] == "node1"
    assert page["has_more"] is False
    assert calls


def test_loader_fetches_wiki_node_underlying_document(monkeypatch):
    """A Wiki URL should resolve to obj_token, fetch the real doc, and keep Wiki metadata."""

    def fake_run(args):
        if args[0:3] == ["api", "GET", "/open-apis/wiki/v2/spaces/get_node"]:
            return {
                "ok": True,
                "data": {
                    "node": {
                        "node_token": "WIKINodeToken1234567890ab",
                        "obj_token": "DOCXToken1234567890abcdef",
                        "obj_type": "docx",
                        "title": "Wiki 页面",
                        "space_id": "1234567890",
                    }
                },
            }
        if args[0:3] == [
            "api",
            "POST",
            "/open-apis/docs_ai/v1/documents/DOCXToken1234567890abcdef/fetch",
        ]:
            assert args[3] == "--data"
            assert json.loads(args[4]) == {
                "export_option": {
                    "export_block_id": False,
                    "export_cite_extra_data": False,
                    "export_style_attrs": False,
                },
                "format": "xml",
            }
            return {
                "ok": True,
                "data": {
                    "document": {
                        "document_id": "DOCXToken1234567890abcdef",
                        "content": "<title>真实文档</title><p>这是知识库里的内容。</p>",
                    }
                },
            }
        raise AssertionError(f"unexpected lark-cli args: {args}")

    monkeypatch.setattr("rag.feishu._run_lark_cli", fake_run)

    docs = FeishuDocLoader(chunk_size=200, chunk_overlap=20).load_and_split(
        "https://xxx.feishu.cn/wiki/WIKINodeToken1234567890ab"
    )

    assert len(docs) == 1
    assert "知识库里的内容" in docs[0].page_content
    assert docs[0].metadata["source"] == "feishu"
    assert docs[0].metadata["feishu_doc_type"] == "docx"
    assert docs[0].metadata["feishu_wiki_node_token"] == "WIKINodeToken1234567890ab"
    assert docs[0].metadata["title"] == "Wiki 页面"


class TestFeishuDefaultSyncer:
    """Verify the full sync pipeline: search → fetch → chunk → vector store."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.loader = FeishuDocLoader()
        from rag.retriever import VectorStoreRetriever
        self.retriever = VectorStoreRetriever()
        self.syncer = FeishuDefaultSyncer(self.loader, self.retriever)

    def test_sync_from_space_returns_summary(self):
        """Syncing from a space returns a list of synced document summaries."""
        from config import settings
        space_id = settings.feishu_default_space_id
        if not space_id:
            pytest.skip("FEISHU_DEFAULT_SPACE_ID not configured")

        results = self.syncer.sync_from_space(space_id)
        assert isinstance(results, list)
        if results:
            doc = results[0]
            assert "token" in doc
            assert "title" in doc
            assert "chunks" in doc

    def test_sync_from_folder_returns_summary(self):
        """Syncing from a folder returns a list of synced document summaries."""
        from config import settings
        folder_token = settings.feishu_default_folder_token
        if not folder_token:
            pytest.skip("FEISHU_DEFAULT_FOLDER_TOKEN not configured")

        results = self.syncer.sync_from_folder(folder_token)
        assert isinstance(results, list)
        if results:
            doc = results[0]
            assert "token" in doc
            assert "chunks" in doc

    def test_sync_errors_are_recorded_not_raised(self):
        """A document that fails to sync should be recorded with an error, not crash the batch."""
        # Use a non-existent space_id that won't have docs — should still return a list
        # (search returns empty results rather than error)
        results = self.syncer._sync_all(space_id="non_existent_space_12345")
        assert isinstance(results, list)

    def test_add_documents_stores_in_memory(self):
        """Documents added via sync should be stored (in-memory fallback)."""
        loader = FeishuDocLoader()

        search = search_feishu_docs(query="test", page_size=1)
        if not search["results"]:
            pytest.skip("No Feishu documents available")
        token = search["results"][0]["result_meta"]["token"]

        try:
            docs = loader.load_and_split(token, title="Integration Test Doc")
        except RuntimeError as exc:
            _skip_if_feishu_external_error(exc)
            raise
        initial_count = len(self.retriever.documents)
        self.retriever.add_documents(docs, status="feishu")

        # Documents should be appended to the in-memory list
        assert len(self.retriever.documents) == initial_count + len(docs)
        for doc in self.retriever.documents[-len(docs):]:
            assert doc.metadata["source"] == "feishu"
            assert doc.metadata["status"] == "feishu"

    def test_synced_documents_are_retrievable(self):
        """Documents added via sync should be searchable in the retriever."""
        loader = FeishuDocLoader()

        search = search_feishu_docs(query="test", page_size=1)
        if not search["results"]:
            pytest.skip("No Feishu documents available")
        token = search["results"][0]["result_meta"]["token"]

        try:
            docs = loader.load_and_split(token, title="Integration Test Doc")
        except RuntimeError as exc:
            _skip_if_feishu_external_error(exc)
            raise
        self.retriever.add_documents(docs, status="feishu")

        try:
            results = self.retriever.similarity_search("test", k=2, status_filter="feishu")
        except Exception as e:
            cls_name = type(e).__name__.lower()
            msg = str(e).lower()
            if any(kw in cls_name or kw in msg for kw in ("timeout", "connect", "timed out")):
                pytest.skip(f"OpenAI API not reachable: {e}")
            raise

        assert len(results) > 0
        for r in results:
            assert r.metadata["source"] == "feishu"
            assert r.metadata["status"] == "feishu"
