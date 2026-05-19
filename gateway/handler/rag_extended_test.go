package handler

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestRagUploadProxiesToAIService(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/rag/upload" {
			t.Errorf("expected path /api/v1/rag/upload, got %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"status":"uploaded"}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewRAGHandler(aiService.URL)
	router.POST("/api/v1/rag/upload", handler.RagUpload)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/rag/upload",
		strings.NewReader("file content"))
	req.Header.Set("Content-Type", "multipart/form-data")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "uploaded") {
		t.Errorf("expected 'uploaded' in response, got: %s", rec.Body.String())
	}
}

func TestRagDocumentsListsDocuments(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/rag/documents" {
			t.Errorf("expected path /api/v1/rag/documents, got %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"documents":[]}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewRAGHandler(aiService.URL)
	router.GET("/api/v1/rag/documents", handler.RagDocuments)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/rag/documents", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
}

func TestRagHealthReturnsOk(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/api/v1/rag/health" {
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			_, _ = w.Write([]byte(`{"status":"ok","storage":"memory","documents":5}`))
			return
		}
		http.NotFound(w, r)
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewRAGHandler(aiService.URL)
	router.GET("/api/v1/rag/health", handler.RagHealth)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/rag/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
}

func TestRagHealthFallsBackToGeneralHealth(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/api/v1/rag/health" {
			http.NotFound(w, r)
			return
		}
		if r.URL.Path == "/health" {
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			_, _ = w.Write([]byte(`{"status":"ok"}`))
			return
		}
		http.NotFound(w, r)
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewRAGHandler(aiService.URL)
	router.GET("/api/v1/rag/health", handler.RagHealth)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/rag/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}

	var body map[string]string
	if err := json.Unmarshal(rec.Body.Bytes(), &body); err != nil {
		t.Fatalf("failed to parse JSON: %v", err)
	}
	if body["fallback"] != "ai-service-health" {
		t.Errorf("expected fallback response, got: %v", body)
	}
}

func TestFeishuSyncProxiesToAIService(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/rag/feishu/sync" {
			t.Errorf("expected /api/v1/rag/feishu/sync, got %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"status":"synced"}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewRAGHandler(aiService.URL)
	router.POST("/api/v1/rag/feishu/sync", handler.FeishuSync)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/rag/feishu/sync",
		strings.NewReader(`{"doc_token":"123"}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "synced") {
		t.Errorf("expected 'synced' in response, got: %s", rec.Body.String())
	}
}

func TestFeishuDefaultSyncProxiesToAIService(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/rag/feishu/default-sync" {
			t.Errorf("expected /api/v1/rag/feishu/default-sync, got %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"status":"synced"}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewRAGHandler(aiService.URL)
	router.POST("/api/v1/rag/feishu/default-sync", handler.FeishuDefaultSync)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/rag/feishu/default-sync",
		strings.NewReader(`{}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
}

func TestRagQueryAIServiceErrorNonStream(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = w.Write([]byte(`{"error":"internal error"}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewRAGHandler(aiService.URL)
	router.POST("/api/v1/rag/query", handler.RagQuery)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/rag/query",
		strings.NewReader(`{"question":"non-direct question"}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	// Should proxy the error response
	if rec.Code != http.StatusInternalServerError {
		t.Errorf("expected 500, got %d", rec.Code)
	}
}

func TestRagQueryAIServiceUnreachable(t *testing.T) {
	gin.SetMode(gin.TestMode)

	router := gin.New()
	handler := NewRAGHandler("http://127.0.0.1:1")
	router.POST("/api/v1/rag/query", handler.RagQuery)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/rag/query",
		strings.NewReader(`{"question":"test"}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusServiceUnavailable {
		t.Errorf("expected 503, got %d", rec.Code)
	}
}

func TestDirectRagAnswer你好(t *testing.T) {
	answer := directRagAnswerFromBody([]byte(`{"question":"你好"}`))
	if answer == "" {
		t.Fatal("expected non-empty answer for '你好'")
	}
	if !strings.Contains(answer, "AI Hiking") {
		t.Errorf("expected answer to contain AI Hiking, got: %s", answer)
	}
}

func TestDirectRagAnswer你是谁(t *testing.T) {
	answer := directRagAnswerFromBody([]byte(`{"question":"你是谁"}`))
	if answer == "" {
		t.Fatal("expected non-empty answer for '你是谁'")
	}
	if !strings.Contains(answer, "RAG 助手") {
		t.Errorf("expected answer to mention RAG 助手, got: %s", answer)
	}
}

func TestDirectRagAnswer谢谢(t *testing.T) {
	answer := directRagAnswerFromBody([]byte(`{"question":"谢谢"}`))
	if answer == "" {
		t.Fatal("expected non-empty answer for '谢谢'")
	}
	if !strings.Contains(answer, "不客气") {
		t.Errorf("expected '不客气' in answer, got: %s", answer)
	}
}

func TestDirectRagAnswerHello(t *testing.T) {
	answer := directRagAnswerFromBody([]byte(`{"question":"hello"}`))
	if answer == "" {
		t.Fatal("expected non-empty answer for 'hello'")
	}
}

func TestDirectRagAnswerUnknownReturnsEmpty(t *testing.T) {
	answer := directRagAnswerFromBody([]byte(`{"question":"some unknown question about hiking routes"}`))
	if answer != "" {
		t.Errorf("expected empty for unknown question, got: %s", answer)
	}
}

func TestDirectRagAnswerInvalidBodyReturnsEmpty(t *testing.T) {
	answer := directRagAnswerFromBody([]byte(`not json`))
	if answer != "" {
		t.Errorf("expected empty for invalid JSON, got: %s", answer)
	}
}

func TestRagKnowledgeBaseIsEmptyHealthCheckFails(t *testing.T) {
	// When the health endpoint is unreachable, isEmpty should return false (safe default)
	handler := NewRAGHandler("http://127.0.0.1:1")
	empty := handler.ragKnowledgeBaseIsEmpty(nil)
	if empty {
		t.Error("expected false when health check fails, got true")
	}
}

func TestIsRagEmbeddingNotFoundLine(t *testing.T) {
	tests := []struct {
		line string
		want bool
	}{
		{`data: {"type":"error","content":"Error code: 404"}`, true},
		{`data: {"type":"error","content":"Error code: 500"}`, false},
		{`data: {"type":"text","content":"Error code: 404"}`, false},
		{`data: {"type":"done"}`, false},
		{"", false},
	}

	for _, tt := range tests {
		got := isRagEmbeddingNotFoundLine(tt.line)
		if got != tt.want {
			t.Errorf("isRagEmbeddingNotFoundLine(%q) = %v, want %v", tt.line, got, tt.want)
		}
	}
}

func TestNewRAGHandler(t *testing.T) {
	handler := NewRAGHandler("http://test:8000")
	if handler == nil {
		t.Fatal("expected non-nil handler")
	}
}
