"""飞书文档集成模块（基于 lark-cli）。

通过 lark-cli 命令行工具接入飞书云文档：
- FeishuDocLoader：单文档抓取 + 分块
- FeishuDefaultSyncer：从空间/文件夹批量同步文档到 RAG 向量存储

lark-cli 自行管理认证，无需在代码中配置 app_id / app_secret。
"""

import json
import logging
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote

_LARK_CLI_PATH = shutil.which("lark-cli") or "lark-cli"

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger("ai-service.rag.feishu")

# 文档 / Wiki URL 中提取 token 的正则
# 示例:
# - https://xxx.feishu.cn/docx/AbCdEf1234567890abcdef
# - https://xxx.feishu.cn/wiki/WIKINodeToken1234567890ab
DOC_TOKEN_RE = re.compile(r"/(docx?|bitable|base|sheets?|slides|mindnote)/([A-Za-z0-9_-]{12,})")
WIKI_NODE_RE = re.compile(r"/wiki/([A-Za-z0-9_-]{12,})")
WIKI_SPACE_RE = re.compile(r"(?:/wiki/(?:space|spaces)/|[?&]space_id=)([A-Za-z0-9_-]{6,})")
FEISHU_URL_RE = re.compile(r"https?://[^\s<>'\"]*feishu\.cn/[^\s<>'\"]+")
SUPPORTED_FETCH_TYPES = {"doc", "docx", "file"}
_DOWNLOADABLE_TYPES = {"file", "md", "txt", "csv", "markdown"}

# lark-cli 子进程超时（秒）
_LARK_CLI_TIMEOUT = 30


@dataclass(frozen=True)
class FeishuLinkInfo:
    """Screened Feishu link/token information."""

    raw: str
    kind: str
    token: str
    doc_type: str = "docx"


def _run_lark_cli(args: list[str]) -> dict:
    """执行 lark-cli 命令并解析 JSON 输出。

    Args:
        args: lark-cli 子命令参数列表，不含 "lark-cli" 本身。

    Returns:
        解析后的 JSON 响应。

    Raises:
        RuntimeError: lark-cli 执行失败或返回错误。
    """
    cmd = [_LARK_CLI_PATH] + args + ["--format", "json"]
    logger.debug("执行 lark-cli: %s", " ".join(cmd))

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=_LARK_CLI_TIMEOUT,
            encoding="utf-8",
        )
    except FileNotFoundError:
        raise RuntimeError("lark-cli 未安装或不在 PATH 中")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"lark-cli 命令超时（{_LARK_CLI_TIMEOUT}s）: {' '.join(cmd)}")

    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        raise RuntimeError(f"lark-cli 执行失败: {stderr}")

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"lark-cli 返回非 JSON 数据: {e}")

    if not data.get("ok") and not data.get("saved_path"):
        raw_error = data.get("error")
        if isinstance(raw_error, dict):
            error_msg = raw_error.get("message") or raw_error.get("type") or "unknown"
            if raw_error.get("hint"):
                error_msg = f"{error_msg}；{raw_error['hint']}"
        else:
            error_msg = data.get("msg", raw_error or "unknown")
        raise RuntimeError(f"lark-cli API 错误: {error_msg}")

    return data


def call_lark_api(
    method: str,
    path: str,
    params: dict | None = None,
    data: dict | None = None,
) -> dict:
    """Call Feishu OpenAPI through lark-cli's generic api command."""
    args = ["api", method.upper(), path]
    if params:
        args.extend(["--params", json.dumps(params, ensure_ascii=False)])
    if data is not None:
        args.extend(["--data", json.dumps(data, ensure_ascii=False)])
    return _run_lark_cli(args)


def _html_to_text(html: str) -> str:
    """将 HTML/XML 转换为纯文本。

    lark-cli docs_ai fetch 返回 XML/HTML 格式文档内容，需要用此函数提取可读文本。
    """
    if not html.strip():
        return ""

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    # 移除 <style> 和 <script> 标签
    for tag in soup(["style", "script"]):
        tag.decompose()
    return soup.get_text()


def _normalize_doc_type(doc_type: str) -> str:
    normalized = doc_type.lower()
    if normalized == "sheets":
        return "sheet"
    if normalized == "base":
        return "bitable"
    if normalized == "file":
        return "file"
    return normalized


def find_feishu_links(text: str) -> list[FeishuLinkInfo]:
    """Find Feishu URLs in free text and classify them."""
    links: list[FeishuLinkInfo] = []
    for match in FEISHU_URL_RE.finditer(text):
        try:
            links.append(inspect_feishu_link(match.group(0)))
        except ValueError:
            continue
    return links


def inspect_feishu_link(url_or_token: str) -> FeishuLinkInfo:
    """Classify a Feishu URL or token before fetching content."""
    value = url_or_token.strip()
    if not value:
        raise ValueError("飞书链接为空")

    doc_match = DOC_TOKEN_RE.search(value)
    if doc_match:
        return FeishuLinkInfo(
            raw=value,
            kind="document",
            token=doc_match.group(2),
            doc_type=_normalize_doc_type(doc_match.group(1)),
        )

    wiki_match = WIKI_NODE_RE.search(value)
    if wiki_match:
        return FeishuLinkInfo(
            raw=value,
            kind="wiki_node",
            token=wiki_match.group(1),
            doc_type="wiki",
        )

    space_match = WIKI_SPACE_RE.search(value)
    if space_match:
        return FeishuLinkInfo(
            raw=value,
            kind="wiki_space",
            token=space_match.group(1),
            doc_type="wiki",
        )

    if "://" in value or "feishu.cn" in value:
        raise ValueError(f"无法从 URL 中提取文档 token: {url_or_token}")

    if value.lower().startswith("wiki") or value.lower().startswith("wik"):
        return FeishuLinkInfo(raw=value, kind="wiki_node", token=value, doc_type="wiki")

    return FeishuLinkInfo(raw=value, kind="document", token=value, doc_type="docx")


def extract_doc_token(url_or_token: str) -> str:
    """从飞书 URL 或直接传入的 doc_token 中提取文档 token。

    如果输入包含 '/' 则视为 URL 进行正则匹配，否则直接返回原值。
    """
    try:
        return inspect_feishu_link(url_or_token).token
    except ValueError:
        if "://" in url_or_token or "feishu.cn" in url_or_token:
            raise
        return url_or_token


def resolve_wiki_node(node_token: str, obj_type: str = "wiki") -> dict:
    """Resolve a Wiki node token to its underlying cloud-document token."""
    params = {"token": node_token}
    if obj_type:
        params["obj_type"] = obj_type

    data = call_lark_api(
        "GET",
        "/open-apis/wiki/v2/spaces/get_node",
        params=params,
    )
    node = data.get("data", {}).get("node", {})
    if not node.get("obj_token"):
        raise RuntimeError(f"飞书 Wiki 节点未返回实际文档 token: {node_token}")
    return node


def list_wiki_nodes(
    space_id: str,
    parent_node_token: str = "",
    page_size: int = 50,
    page_token: str = "",
) -> dict:
    """List Wiki nodes in a space or under a parent node."""
    params = {
        "page_size": max(1, min(page_size, 50)),
    }
    if parent_node_token:
        params["parent_node_token"] = parent_node_token
    if page_token:
        params["page_token"] = page_token

    data = call_lark_api(
        "GET",
        f"/open-apis/wiki/v2/spaces/{quote(space_id, safe='')}/nodes",
        params=params,
    )
    inner = data.get("data", {})
    return {
        "items": inner.get("items", []),
        "has_more": inner.get("has_more", False),
        "page_token": inner.get("page_token", ""),
    }


def walk_wiki_nodes(space_id: str, max_pages: int = 200) -> list[dict]:
    """Walk a Wiki space tree breadth-first and return all visible nodes."""
    nodes: list[dict] = []
    queue: list[str] = [""]
    pages = 0

    while queue and pages < max_pages:
        parent = queue.pop(0)
        page_token = ""

        while pages < max_pages:
            pages += 1
            page = list_wiki_nodes(
                space_id=space_id,
                parent_node_token=parent,
                page_token=page_token,
            )

            for node in page["items"]:
                nodes.append(node)
                if node.get("has_child") and node.get("node_token"):
                    queue.append(node["node_token"])

            if not page["has_more"]:
                break
            page_token = page["page_token"]

    return nodes


class FeishuDocLoader:
    """飞书文档加载器：通过 lark-cli 抓取文档内容 → 分块 → 返回 LangChain Document 列表。

    用法:
        loader = FeishuDocLoader()
        docs = loader.load_and_split("AbCdEf1234567890abcdef", title="需求文档")
        retriever.add_documents(docs, status="feishu")
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", ".", " ", ""],
        )

    def download_file(self, file_token: str) -> dict:
        """通过 drive API 下载 file 类型文档。

        Args:
            file_token: 飞书文件 token。

        Returns:
            {"markdown": str, "title": str, "doc_id": str}
        """
        data = call_lark_api(
            "GET",
            f"/open-apis/drive/v1/files/{quote(file_token, safe='')}/download",
        )
        saved_path = data.get("saved_path", "")
        content_type = data.get("content_type", "")

        text = ""
        if saved_path:
            try:
                with open(saved_path, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except Exception as e:
                logger.warning("读取下载文件失败: %s", e)

        title = ""
        if saved_path:
            from pathlib import Path
            title = Path(saved_path).stem

        return {
            "markdown": text,
            "title": title,
            "doc_id": file_token,
        }

    def fetch_content(self, doc_token: str, doc_type: str = "docx") -> dict:
        """通过 lark-cli API 获取文档内容。

        对于 file 类型文档，使用 drive download 下载；
        对于 doc/docx 类型文档，使用 docs_ai fetch 抓取。

        Args:
            doc_token: 飞书文档 token。
            doc_type: 文档类型。

        Returns:
            {"markdown": str, "title": str, "doc_id": str}
        """
        if doc_type in _DOWNLOADABLE_TYPES:
            return self.download_file(doc_token)

        body = {
            "export_option": {
                "export_block_id": False,
                "export_cite_extra_data": False,
                "export_style_attrs": False,
            },
            "format": "xml",
        }
        data = call_lark_api(
            "POST",
            f"/open-apis/docs_ai/v1/documents/{quote(doc_token, safe='')}/fetch",
            data=body,
        )
        inner = data.get("data", {})
        document = inner.get("document", inner)

        html_content = (
            document.get("content")
            or document.get("markdown")
            or document.get("text")
            or inner.get("content")
            or ""
        )
        doc_id = document.get("document_id") or inner.get("document_id") or doc_token

        title = document.get("title") or inner.get("title") or ""
        title_match = re.search(r"<title>(.*?)</title>", html_content)
        if title_match and not title:
            title = title_match.group(1)

        text = _html_to_text(html_content)
        return {
            "markdown": text,
            "title": title,
            "doc_id": doc_id,
        }

    def _resolve_document_ref(self, doc_ref: str, doc_type: str = "docx") -> tuple[str, str, dict]:
        """Resolve a document URL/token into fetchable doc token, type, and metadata."""
        link = inspect_feishu_link(doc_ref)
        metadata: dict = {}

        if link.kind == "wiki_space":
            raise ValueError("检测到飞书知识库空间链接，请使用知识库同步入口或提供具体 Wiki 页面链接")

        if link.kind == "wiki_node":
            try:
                node = resolve_wiki_node(link.token)
                obj_type = _normalize_doc_type(node.get("obj_type", "docx"))
                metadata.update({
                    "feishu_wiki_node_token": node.get("node_token", link.token),
                    "feishu_space_id": node.get("space_id", ""),
                    "feishu_obj_token": node.get("obj_token", ""),
                    "title": node.get("title", ""),
                })
                if obj_type in SUPPORTED_FETCH_TYPES:
                    return node["obj_token"], obj_type, metadata
                if obj_type not in _DOWNLOADABLE_TYPES:
                    raise RuntimeError(f"暂不支持读取 Wiki 节点类型: {obj_type}")
                return node["obj_token"], obj_type, metadata
            except RuntimeError as e:
                if "99991679" in str(e) or "Permission denied" in str(e):
                    logger.warning("Wiki API 权限不足，降级为直接下载: %s", link.token)
                    metadata["feishu_wiki_node_token"] = link.token
                    return link.token, "file", metadata
                raise

        resolved_type = _normalize_doc_type(doc_type or link.doc_type)
        if resolved_type == "wiki":
            resolved_type = link.doc_type
        if resolved_type not in SUPPORTED_FETCH_TYPES and resolved_type not in _DOWNLOADABLE_TYPES:
            raise RuntimeError(f"暂不支持读取飞书文档类型: {resolved_type}")
        return link.token, resolved_type, metadata

    def load_and_split(
        self,
        doc_token: str,
        title: str = "",
        doc_type: str = "docx",
    ) -> list[Document]:
        """抓取并拆分飞书文档为 LangChain Document 列表。

        Args:
            doc_token: 飞书文档 token。
            title: 文档标题，默认使用飞书 API 返回的标题。
            doc_type: 文档类型，写入 metadata 备用。

        Returns:
            拆分后的 Document 列表。
        """
        resolved_token, resolved_type, extra_metadata = self._resolve_document_ref(doc_token, doc_type)
        fetched = self.fetch_content(resolved_token, doc_type=resolved_type)
        content = fetched["markdown"]
        doc_title = title or extra_metadata.get("title") or fetched["title"] or resolved_token

        if not content.strip():
            logger.warning("飞书文档 %s 内容为空", resolved_token)
            return []

        docs = self.splitter.create_documents([content])

        for doc in docs:
            doc.metadata["source"] = "feishu"
            doc.metadata["feishu_doc_token"] = resolved_token
            doc.metadata["feishu_doc_type"] = resolved_type
            doc.metadata["title"] = doc_title
            doc.metadata.update({k: v for k, v in extra_metadata.items() if v})

        logger.info(
            "飞书文档 %s (%s) → %d 个块",
            resolved_token,
            doc_title,
            len(docs),
        )
        return docs


def search_feishu_docs(
    query: str = "",
    space_id: str = "",
    folder_token: str = "",
    page_size: int = 20,
    page_token: str = "",
) -> dict:
    """搜索飞书空间中的文档。

    Args:
        query: 搜索关键词，空字符串表示浏览全部。
        space_id: 知识库空间 ID（与 folder_token 互斥）。
        folder_token: 文件夹 token（与 space_id 互斥）。
        page_size: 每页数量（1-20）。
        page_token: 翻页 token。

    Returns:
        {"results": [...], "has_more": bool, "page_token": str, "total": int}
    """
    args = ["drive", "+search", "--page-size", str(page_size)]

    if query:
        args += ["--query", query]
    if space_id:
        args += ["--space-ids", space_id]
    if folder_token:
        args += ["--folder-tokens", folder_token]
    if page_token:
        args += ["--page-token", page_token]

    data = _run_lark_cli(args)
    inner = data.get("data", {})
    return {
        "results": inner.get("results", []),
        "has_more": inner.get("has_more", False),
        "page_token": inner.get("page_token", ""),
        "total": inner.get("total", 0),
    }


class FeishuDefaultSyncer:
    """飞书默认文档同步器：从配置的空间/文件夹批量拉取文档并同步到向量存储。

    用法:
        syncer = FeishuDefaultSyncer(loader, retriever)
        result = syncer.sync_from_space("space_id_xxx")
        # 或
        result = syncer.sync_from_folder("folder_token_xxx")
    """

    def __init__(self, loader: FeishuDocLoader, retriever):
        self.loader = loader
        self.retriever = retriever

    def sync_from_space(self, space_id: str) -> list[dict]:
        """从知识库空间同步所有文档。

        Args:
            space_id: 知识库空间 ID。

        Returns:
            已同步的文档摘要列表。
        """
        return self._sync_all(space_id=space_id)

    def sync_from_folder(self, folder_token: str) -> list[dict]:
        """从文件夹同步所有文档。

        Args:
            folder_token: 文件夹 token。

        Returns:
            已同步的文档摘要列表。
        """
        return self._sync_all(folder_token=folder_token)

    def _sync_all(
        self,
        space_id: str = "",
        folder_token: str = "",
    ) -> list[dict]:
        """遍历所有页面并逐文档同步。"""
        if space_id:
            return self._sync_wiki_space(space_id)

        synced: list[dict] = []
        page_token = ""
        page = 0

        while True:
            page += 1
            logger.info("搜索飞书文档 [第 %d 页]...", page)

            result = search_feishu_docs(
                space_id=space_id,
                folder_token=folder_token,
                page_token=page_token,
            )

            for item in result["results"]:
                meta = item.get("result_meta", {})
                doc_token = meta.get("token", "")
                doc_type = meta.get("doc_types", "docx").lower()
                doc_title = meta.get("title_highlighted", "")

                if not doc_token:
                    continue

                if doc_type == "file":
                    icon_info_str = meta.get("icon_info", "")
                    if icon_info_str:
                        try:
                            icon_info = json.loads(icon_info_str)
                            file_token = icon_info.get("token", "")
                            if file_token:
                                doc_token = file_token
                        except (json.JSONDecodeError, TypeError):
                            pass

                try:
                    docs = self.loader.load_and_split(
                        doc_token=doc_token,
                        title=doc_title,
                        doc_type=doc_type,
                    )
                    self.retriever.add_documents(docs, status="feishu")
                    synced.append({
                        "token": doc_token,
                        "title": doc_title,
                        "chunks": len(docs),
                    })
                    time.sleep(0.3)  # 请求间隔，避免触发频率限制
                except Exception as e:
                    logger.error("同步文档 %s 失败: %s", doc_token, e)
                    synced.append({
                        "token": doc_token,
                        "title": doc_title,
                        "chunks": 0,
                        "error": str(e),
                    })

            if not result["has_more"]:
                break
            page_token = result["page_token"]

        logger.info("飞书默认同步完成：%d 篇文档", len(synced))
        return synced

    def _sync_wiki_space(self, space_id: str) -> list[dict]:
        """Traverse a Wiki knowledge base and sync supported document nodes."""
        synced: list[dict] = []
        try:
            nodes = walk_wiki_nodes(space_id)
        except Exception as e:
            logger.error("遍历飞书 Wiki 空间 %s 失败: %s", space_id, e)
            return [{
                "token": space_id,
                "title": "",
                "chunks": 0,
                "error": str(e),
            }]

        for node in nodes:
            doc_type = _normalize_doc_type(node.get("obj_type", ""))
            node_token = node.get("node_token", "")
            doc_title = node.get("title", "")

            if not node_token:
                continue
            if doc_type not in SUPPORTED_FETCH_TYPES and doc_type not in _DOWNLOADABLE_TYPES:
                synced.append({
                    "token": node_token,
                    "title": doc_title,
                    "chunks": 0,
                    "error": f"暂不支持读取 Wiki 节点类型: {doc_type or 'unknown'}",
                })
                continue

            try:
                docs = self.loader.load_and_split(
                    doc_token=node_token,
                    title=doc_title,
                    doc_type="wiki",
                )
                self.retriever.add_documents(docs, status="feishu")
                synced.append({
                    "token": node_token,
                    "title": doc_title,
                    "chunks": len(docs),
                })
                time.sleep(0.3)
            except Exception as e:
                logger.error("同步 Wiki 节点 %s 失败: %s", node_token, e)
                synced.append({
                    "token": node_token,
                    "title": doc_title,
                    "chunks": 0,
                    "error": str(e),
                })

        logger.info("飞书 Wiki 空间同步完成：%d 个节点", len(synced))
        return synced
