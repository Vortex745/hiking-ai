package handler

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestRagQueryFallsBackForEmptyMemoryEmbedding404(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/api/v1/rag/health":
			w.Header().Set("Content-Type", "application/json")
			_, _ = w.Write([]byte(`{"status":"ok","storage":"memory","documents":0}`))
		case "/api/v1/rag/query":
			w.Header().Set("Content-Type", "text/event-stream")
			_, _ = w.Write([]byte(`data: {"type": "thought", "content": "正在检索相关知识库..."}` + "\n\n"))
			_, _ = w.Write([]byte(`data: {"type": "error", "content": "Error code: 404"}` + "\n\n"))
		default:
			http.NotFound(w, r)
		}
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewRAGHandler(aiService.URL)
	router.POST("/api/v1/rag/query", handler.RagQuery)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/rag/query", strings.NewReader(`{"question":"测试 RAG","status":"feishu"}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	router.ServeHTTP(rec, req)

	body := rec.Body.String()
	if strings.Contains(body, "Error code: 404") {
		t.Fatalf("expected empty knowledge base fallback, got backend error stream: %s", body)
	}
	if !strings.Contains(body, "知识库中没有找到相关文档") {
		t.Fatalf("expected no-document message, got: %s", body)
	}
	if !strings.Contains(body, "调用 embedding 模型生成查询向量") {
		t.Fatalf("expected embedding process step, got: %s", body)
	}
	if !strings.Contains(body, "使用向量在 pgvector/memory 中召回候选片段") {
		t.Fatalf("expected vector retrieval process step, got: %s", body)
	}
	if !strings.Contains(body, `"type":"done"`) {
		t.Fatalf("expected done event, got: %s", body)
	}
}

func TestRagQueryDirectAnswerSkipsAIService(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiServiceCalled := false
	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		aiServiceCalled = true
		http.Error(w, "should not be called", http.StatusInternalServerError)
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewRAGHandler(aiService.URL)
	router.POST("/api/v1/rag/query", handler.RagQuery)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/rag/query", strings.NewReader(`{"question":"你好"}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	router.ServeHTTP(rec, req)

	body := rec.Body.String()
	if aiServiceCalled {
		t.Fatalf("expected direct answer without calling AI service")
	}
	if strings.Contains(body, "正在检索相关知识库") {
		t.Fatalf("expected no retrieval thought, got: %s", body)
	}
	if !strings.Contains(body, "AI Hiking") {
		t.Fatalf("expected direct assistant response, got: %s", body)
	}
	if !strings.Contains(body, `"type":"done"`) {
		t.Fatalf("expected done event, got: %s", body)
	}
}
