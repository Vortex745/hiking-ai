# Agent 三层记忆架构 — 实现文档

## 1. 项目概述

### 1.1 目标

给 AI Agent 加上跨会话记忆。对话一长就超窗口、丢信息，这是个老问题。

### 1.2 思路

把记忆按时效性分三层：当前会话直接用原文，近期的压成摘要，长期知识存下来按需检索。全量加载 100 轮对话大概 50k tokens，压缩后不到 3k。

| 层 | 名称 | 时效 | Token 量 | 怎么存 |
|---|------|------|----------|--------|
| L0 | 工作记忆 | 当前会话 | 不限 | 对话原文直接放 prompt |
| L1 | 压缩记忆 | 近期会话 | ~500t/会话 | LLM 生成的摘要，JSON 文件 |
| L2 | 长期记忆 | 跨所有会话 | ~100t/条 | 结构化知识 + 向量索引 |

### 1.3 技术来源

| 本方案 | 来自哪 | 改了什么 |
|-------|--------|---------|
| L1 语义摘要 | Claude-Mem | 只留会话结束压缩，去掉了 6 个生命周期钩子 |
| L2 结构化知识 | OpenViking | 8 类缩到 3 类 |
| 向量检索 | 两者 | 扁平检索，不做目录递归 |
| Viking URI / 路径锁 / RedoLog | OpenViking | 没用，太重了 |

---

## 2. 系统架构

### 2.1 整体结构

```
┌─────────────────────────────────────────────────┐
│                   Agent 会话                     │
│                                                  │
│  Prompt 组装                                     │
│  ┌───────────────────────────────────────────┐  │
│  │ [System] + [L0 当前对话] + [L1 近期摘要]   │  │
│  │ + [L2 检索到的知识] + [用户输入]           │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  会话结束                                        │
│  ┌───────────────────────────────────────────┐  │
│  │ 对话历史 → 压缩摘要(L1) → 提取知识(L2)     │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### 2.2 数据流

写入（会话结束时）：

```
对话历史
  │
  ├─► LLM 压缩 ──► 会话摘要 ──► sessions/
  │
  └─► LLM 提取 ──► 结构化知识 ──► knowledge/
                                  ──► 向量化 ──► index/
```

读取（新会话启动时）：

```
1. L0：当前会话最近 N 轮（自动）
2. L1：最近 1~2 个摘要文件（直接读）
3. L2：用户输入 → embedding → 向量检索 → 相关知识
4. 组装：L0 + L1 + L2 + 用户输入
```

---

## 3. 目录结构与数据格式

### 3.1 目录

```
memory/
├── sessions/                   # L1：会话压缩摘要
│   ├── 2026-05-15.json
│   └── 2026-05-16.json
├── knowledge/                  # L2：结构化长期记忆
│   ├── preferences.json        # 用户偏好
│   ├── projects.json           # 项目背景
│   └── lessons.json            # 经验教训
└── index/                      # L2：向量索引
    ├── embeddings.faiss
    └── id_map.json             # 向量 ID → 知识条目映射
```

### 3.2 L1 会话摘要

`memory/sessions/YYYY-MM-DD.json`

```json
{
  "date": "2026-05-16",
  "summary": "用户在开发一个 RAG 项目，讨论了长上下文管理方案。最终采用三层记忆架构，融合 OpenViking 的分级加载和 Claude-Mem 的语义摘要压缩。",
  "topics": ["RAG", "长上下文", "记忆架构", "OpenViking", "Claude-Mem"],
  "decisions": [
    "采用三层记忆架构（L0/L1/L2）",
    "L1 用 LLM 语义摘要压缩",
    "L2 简化为 3 类知识"
  ],
  "action_items": ["实现完整代码", "写简历 demo"],
  "token_count_original": 15000,
  "token_count_summary": 300,
  "compression_ratio": 0.02
}
```

### 3.3 L2 结构化知识

`memory/knowledge/preferences.json`

```json
[
  {
    "id": "pref_001",
    "category": "coding_style",
    "content": "用户偏好 Python，喜欢类型注解和 docstring",
    "source_session": "2026-05-15",
    "confidence": 0.9,
    "updated_at": "2026-05-15T18:30:00"
  }
]
```

`memory/knowledge/projects.json`

```json
[
  {
    "id": "proj_001",
    "name": "RAG 三层记忆",
    "description": "基于 L0/L1/L2 的 Agent 上下文记忆系统",
    "tech_stack": ["Python", "FAISS", "OpenAI API"],
    "key_decisions": [
      "三层架构而非全量存储",
      "LLM 压缩而非截断"
    ],
    "source_session": "2026-05-16",
    "updated_at": "2026-05-16T18:40:00"
  }
]
```

`memory/knowledge/lessons.json`

```json
[
  {
    "id": "lesson_001",
    "type": "success",
    "content": "LLM 压缩摘要比截断效果好，信息密度高且语义完整",
    "source_session": "2026-05-16",
    "updated_at": "2026-05-16T18:40:00"
  },
  {
    "id": "lesson_002",
    "type": "failure",
    "content": "全量加载历史对话 Token 消耗太大，100 轮约 50k tokens",
    "source_session": "2026-05-16",
    "updated_at": "2026-05-16T18:40:00"
  }
]
```

### 3.4 L2 向量索引映射

`memory/index/id_map.json`

```json
{
  "0": {"knowledge_type": "preferences", "entry_id": "pref_001"},
  "1": {"knowledge_type": "projects", "entry_id": "proj_001"},
  "2": {"knowledge_type": "lessons", "entry_id": "lesson_001"}
}
```

---

## 4. 核心模块实现

### 4.1 配置

```python
# config.py
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class MemoryConfig:
    base_dir: Path = Path("./memory")
    sessions_dir: Path = field(init=False)
    knowledge_dir: Path = field(init=False)
    index_dir: Path = field(init=False)

    # L0
    max_recent_turns: int = 10

    # L1
    max_session_summaries: int = 5
    summary_max_tokens: int = 500

    # L2
    top_k: int = 5
    similarity_threshold: float = 0.7

    # LLM
    llm_model: str = "gpt-4o-mini"
    llm_api_base: str = "https://api.openai.com/v1"
    llm_api_key: str = ""

    # Embedding
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536

    def __post_init__(self):
        self.sessions_dir = self.base_dir / "sessions"
        self.knowledge_dir = self.base_dir / "knowledge"
        self.index_dir = self.base_dir / "index"
```

### 4.2 L1 会话压缩

```python
# compressor.py
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI

class SessionCompressor:
    """把对话历史压成结构化摘要"""

    SUMMARY_PROMPT = """将以下对话历史压缩为结构化摘要。

输出 JSON，字段：
1. summary: 简洁摘要（不超过 300 字）
2. topics: 主要话题关键词（3~8 个）
3. decisions: 关键决策（如有）
4. action_items: 后续待办（如有）

对话历史：
{conversation}

只输出 JSON。"""

    def __init__(self, config):
        self.config = config
        self.client = OpenAI(
            base_url=config.llm_api_base,
            api_key=config.llm_api_key
        )

    def compress(self, messages: list[dict]) -> dict:
        conversation = self._format_messages(messages)

        response = self.client.chat.completions.create(
            model=self.config.llm_model,
            messages=[
                {"role": "system", "content": "你是对话压缩助手，只输出 JSON。"},
                {"role": "user", "content": self.SUMMARY_PROMPT.format(
                    conversation=conversation
                )}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )

        result = json.loads(response.choices[0].message.content)

        original_tokens = sum(len(m.get("content", "")) // 4 for m in messages)
        summary_tokens = len(result.get("summary", "")) // 4

        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": result.get("summary", ""),
            "topics": result.get("topics", []),
            "decisions": result.get("decisions", []),
            "action_items": result.get("action_items", []),
            "token_count_original": original_tokens,
            "token_count_summary": summary_tokens,
            "compression_ratio": round(summary_tokens / max(original_tokens, 1), 3)
        }

    def save(self, summary: dict) -> Path:
        self.config.sessions_dir.mkdir(parents=True, exist_ok=True)
        path = self.config.sessions_dir / f"{summary['date']}.json"
        path.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                        encoding="utf-8")
        return path

    def load_recent(self, n: int = None) -> list[dict]:
        n = n or self.config.max_session_summaries
        files = sorted(self.config.sessions_dir.glob("*.json"), reverse=True)
        return [json.loads(f.read_text(encoding="utf-8")) for f in files[:n]]

    def _format_messages(self, messages: list[dict]) -> str:
        return "\n".join(
            f"[{m.get('role', 'unknown')}] {m.get('content', '')}"
            for m in messages
        )
```

### 4.3 L2 知识提取

```python
# knowledge.py
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI

class KnowledgeExtractor:
    """从对话摘要中提取结构化知识"""

    EXTRACT_PROMPT = """从以下对话摘要中提取三类知识：

1. preferences（用户偏好）: 写作风格、编码习惯、工具偏好
2. projects（项目背景）: 项目名称、技术栈、架构决策
3. lessons（经验教训）: 成功经验(type=success)或失败教训(type=failure)

摘要：{summary}
话题：{topics}

输出 JSON：
{{
  "preferences": [{{"category": "...", "content": "..."}}],
  "projects": [{{"name": "...", "description": "...", "tech_stack": [...], "key_decisions": [...]}}],
  "lessons": [{{"type": "success/failure", "content": "..."}}]
}}

某类没有就返回空数组。"""

    KNOWLEDGE_TYPES = ["preferences", "projects", "lessons"]

    def __init__(self, config):
        self.config = config
        self.client = OpenAI(
            base_url=config.llm_api_base,
            api_key=config.llm_api_key
        )

    def extract(self, session_summary: dict) -> dict:
        response = self.client.chat.completions.create(
            model=self.config.llm_model,
            messages=[
                {"role": "system", "content": "你是知识提取助手，只输出 JSON。"},
                {"role": "user", "content": self.EXTRACT_PROMPT.format(
                    summary=session_summary.get("summary", ""),
                    topics=", ".join(session_summary.get("topics", []))
                )}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        return json.loads(response.choices[0].message.content)

    def save(self, extracted: dict, session_date: str):
        """保存知识，和已有条目合并去重"""
        self.config.knowledge_dir.mkdir(parents=True, exist_ok=True)
        now = datetime.now().isoformat(timespec="seconds")

        for ktype in self.KNOWLEDGE_TYPES:
            path = self.config.knowledge_dir / f"{ktype}.json"
            existing = []
            if path.exists():
                existing = json.loads(path.read_text(encoding="utf-8"))

            new_items = extracted.get(ktype, [])
            for i, item in enumerate(new_items):
                entry_id = f"{ktype[:4]}_{len(existing) + i + 1:03d}"
                item["id"] = entry_id
                item["source_session"] = session_date
                item["updated_at"] = now

                # 同 content 跳过
                contents = {e.get("content", "") for e in existing}
                if item.get("content", "") not in contents:
                    existing.append(item)

            path.write_text(
                json.dumps(existing, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
```

### 4.4 L2 向量索引

```python
# vector_store.py
import json
from pathlib import Path
import numpy as np
from openai import OpenAI

class VectorStore:
    """FAISS 向量存储与检索"""

    def __init__(self, config):
        self.config = config
        self.client = OpenAI(
            base_url=config.llm_api_base,
            api_key=config.llm_api_key
        )
        self.index = None
        self.id_map = {}
        self._load_index()

    def _get_embeddings(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.config.embedding_model,
            input=texts
        )
        return [item.embedding for item in response.data]

    def _load_index(self):
        index_path = self.config.index_dir / "embeddings.faiss"
        map_path = self.config.index_dir / "id_map.json"

        if index_path.exists() and map_path.exists():
            import faiss
            self.index = faiss.read_index(str(index_path))
            self.id_map = json.loads(map_path.read_text(encoding="utf-8"))
        else:
            self._init_empty_index()

    def _init_empty_index(self):
        import faiss
        self.index = faiss.IndexFlatIP(self.config.embedding_dimension)
        self.id_map = {}
        self.config.index_dir.mkdir(parents=True, exist_ok=True)

    def add_knowledge(self, knowledge_type: str, entries: list[dict]):
        if not entries:
            return

        texts = []
        for entry in entries:
            text = entry.get("content", "") or entry.get("description", "")
            if entry.get("tech_stack"):
                text += f" 技术栈: {', '.join(entry['tech_stack'])}"
            texts.append(text)

        embeddings = self._get_embeddings(texts)
        vectors = np.array(embeddings, dtype=np.float32)

        import faiss
        faiss.normalize_L2(vectors)

        start_id = self.index.ntotal
        for i, entry in enumerate(entries):
            self.id_map[str(start_id + i)] = {
                "knowledge_type": knowledge_type,
                "entry_id": entry["id"]
            }

        self.index.add(vectors)
        self._save()

    def search(self, query: str, top_k: int = None) -> list[dict]:
        top_k = top_k or self.config.top_k

        if self.index.ntotal == 0:
            return []

        query_embedding = self._get_embeddings([query])
        query_vector = np.array(query_embedding, dtype=np.float32)

        import faiss
        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or score < self.config.similarity_threshold:
                continue

            map_entry = self.id_map.get(str(idx))
            if not map_entry:
                continue

            ktype = map_entry["knowledge_type"]
            entry_id = map_entry["entry_id"]
            path = self.config.knowledge_dir / f"{ktype}.json"

            if path.exists():
                entries = json.loads(path.read_text(encoding="utf-8"))
                for e in entries:
                    if e["id"] == entry_id:
                        results.append({**e, "score": float(score), "knowledge_type": ktype})
                        break

        return sorted(results, key=lambda x: x["score"], reverse=True)

    def _save(self):
        import faiss
        faiss.write_index(self.index,
                          str(self.config.index_dir / "embeddings.faiss"))
        (self.config.index_dir / "id_map.json").write_text(
            json.dumps(self.id_map, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
```

### 4.5 记忆管理器

```python
# memory_manager.py
import json
from datetime import datetime
from config import MemoryConfig
from compressor import SessionCompressor
from knowledge import KnowledgeExtractor
from vector_store import VectorStore

class MemoryManager:
    """三层记忆统一管理"""

    def __init__(self, config: MemoryConfig = None):
        self.config = config or MemoryConfig()
        self._init_dirs()

        self.compressor = SessionCompressor(self.config)
        self.extractor = KnowledgeExtractor(self.config)
        self.vector_store = VectorStore(self.config)

        self.current_messages = []  # L0 工作记忆

    def _init_dirs(self):
        for d in [self.config.sessions_dir,
                  self.config.knowledge_dir,
                  self.config.index_dir]:
            d.mkdir(parents=True, exist_ok=True)

    # L0

    def add_message(self, role: str, content: str):
        self.current_messages.append({"role": role, "content": content})

    def get_working_memory(self) -> list[dict]:
        return self.current_messages[-self.config.max_recent_turns * 2:]

    # L1

    def get_recent_summaries(self, n: int = None) -> list[dict]:
        return self.compressor.load_recent(n)

    # L2

    def search_knowledge(self, query: str, top_k: int = None) -> list[dict]:
        return self.vector_store.search(query, top_k)

    # Prompt 组装

    def build_prompt(self, user_input: str) -> str:
        parts = []

        summaries = self.get_recent_summaries()
        if summaries:
            summary_text = "\n".join(
                f"- [{s['date']}] {s['summary']}" for s in summaries
            )
            parts.append(f"## 近期会话记忆\n{summary_text}")

        knowledge = self.search_knowledge(user_input)
        if knowledge:
            knowledge_text = "\n".join(
                f"- [{k['knowledge_type']}] {k.get('content') or k.get('description', '')}"
                for k in knowledge
            )
            parts.append(f"## 相关长期记忆\n{knowledge_text}")

        return "\n\n".join(parts) if parts else ""

    # 会话结束

    def end_session(self) -> dict:
        if not self.current_messages:
            return {}

        # L1 压缩
        summary = self.compressor.compress(self.current_messages)
        self.compressor.save(summary)

        # L2 提取
        extracted = self.extractor.extract(summary)
        self.extractor.save(extracted, summary["date"])

        # L2 向量化
        for ktype in KnowledgeExtractor.KNOWLEDGE_TYPES:
            items = extracted.get(ktype, [])
            if items:
                path = self.config.knowledge_dir / f"{ktype}.json"
                all_entries = json.loads(path.read_text(encoding="utf-8"))
                new_ids = {item.get("id") for item in items if item.get("id")}
                new_entries = [e for e in all_entries if e["id"] in new_ids]
                self.vector_store.add_knowledge(ktype, new_entries)

        self.current_messages = []

        return {
            "summary_saved": summary["date"],
            "knowledge_extracted": {
                ktype: len(extracted.get(ktype, []))
                for ktype in KnowledgeExtractor.KNOWLEDGE_TYPES
            },
            "compression_ratio": summary.get("compression_ratio", 0)
        }
```

---

## 5. 使用示例

### 5.1 基本使用

```python
from memory_manager import MemoryManager
from config import MemoryConfig

config = MemoryConfig(
    base_dir=Path("./memory"),
    llm_api_key="sk-xxx",
    llm_model="gpt-4o-mini",
    embedding_model="text-embedding-3-small"
)
memory = MemoryManager(config)

# 会话中：记录消息
memory.add_message("user", "我想做一个 RAG 项目")
memory.add_message("assistant", "好的，你希望 RAG 用在什么场景？")
memory.add_message("user", "用于企业知识库问答")
memory.add_message("assistant", "推荐用 FAISS + GPT-4o-mini 的方案...")

# 新会话：加载记忆
user_input = "上次我们讨论的 RAG 项目，进度怎么样了？"
context = memory.build_prompt(user_input)
# 输出：
# ## 近期会话记忆
# - [2026-05-16] 用户在开发一个 RAG 项目...
# ## 相关长期记忆
# - [projects] 基于 FAISS + GPT-4o-mini 的企业知识库问答系统

full_prompt = f"{context}\n\n用户: {user_input}"

# 会话结束：保存
result = memory.end_session()
# {"summary_saved": "2026-05-16",
#  "knowledge_extracted": {"preferences": 1, "projects": 1, "lessons": 0},
#  "compression_ratio": 0.02}
```

### 5.2 完整对话循环

```python
from openai import OpenAI

client = OpenAI(api_key=config.llm_api_key)

def chat(user_input: str) -> str:
    memory.add_message("user", user_input)

    memory_context = memory.build_prompt(user_input)

    messages = [
        {"role": "system", "content": f"你是一个有记忆的 AI 助手。\n\n{memory_context}"},
        *memory.get_working_memory()
    ]

    response = client.chat.completions.create(
        model=config.llm_model,
        messages=messages
    )
    reply = response.choices[0].message.content

    memory.add_message("assistant", reply)
    return reply

# 使用
print(chat("你好，我是小明"))
print(chat("帮我写一个 Python 爬虫"))
print(chat("记住我喜欢用 type hints"))

# 结束时保存
memory.end_session()
```

---

## 6. 依赖与安装

```txt
# requirements.txt
openai>=1.0.0
faiss-cpu>=1.7.0
numpy>=1.24.0
```

```bash
pip install -r requirements.txt
```

环境变量：

```bash
export OPENAI_API_KEY="sk-xxx"
export OPENAI_API_BASE="https://api.openai.com/v1"
```

---

## 7. Token 消耗对比

| 场景 | 全量加载 | 三层记忆 | 节省 |
|------|---------|---------|------|
| 5 轮对话 | ~5,000t | ~5,000t（L0 全量） | 0% |
| 20 轮对话 | ~20,000t | ~2,000t（L0+L1） | 90% |
| 100 轮对话 | ~50,000t | ~3,000t（L0+L1+L2） | 94% |
| 跨 10 个会话 | ~200,000t | ~4,000t（L1+L2） | 98% |

计算方式：

```
全量 = 所有历史消息 tokens 之和

三层 = L0(最近N轮原文) + L1(最近M个摘要×500) + L2(检索K条×100)
```

5 轮以内 L0 全量就够了，没省头。对话越长，分层优势越明显。

---

## 8. 后续可以做的

- 知识去重：LLM 判断新旧知识是否重复
- 知识衰减：长期没用的知识降权
- 多用户：按 user_id 分目录
- 记忆可视化：Web UI 浏览三层内容
- Rerank：检索结果精排
- 知识迭代：后续会话修正已有条目

---

## 9. 面试怎么说

> 我做了个三层记忆架构：L0 存当前对话原文，L1 用 LLM 把历史对话压成摘要，L2 从摘要里提取结构化知识做向量索引。新会话启动时加载 L1 摘要，再根据用户输入从 L2 语义检索相关知识。比全量加载省 90% 以上 Token。
>
> 为什么分三层？L0 保精度，L1 保连续性，L2 保长期积累。层级越深信息越密，消耗越低。
>
> 压缩用 LLM 而不是截断，因为截断丢语义边界，LLM 压缩能保留话题、决策、待办这些结构化信息。
