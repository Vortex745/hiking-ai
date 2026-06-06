package handler

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestChatSyncProxiesToAIService(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/chat/sync" {
			t.Errorf("expected path /api/v1/chat/sync, got %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"response":"hello"}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewChatHandler(aiService.URL)
	router.POST("/api/v1/chat/sync", handler.ChatSync)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/chat/sync",
		strings.NewReader(`{"message":"hi"}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "hello") {
		t.Errorf("expected response body to contain 'hello', got: %s", rec.Body.String())
	}
}

func TestChatSyncAIUnreachable(t *testing.T) {
	gin.SetMode(gin.TestMode)

	handler := NewChatHandler("http://127.0.0.1:1")

	router := gin.New()
	router.POST("/api/v1/chat/sync", handler.ChatSync)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/chat/sync",
		strings.NewReader(`{"message":"hi"}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusServiceUnavailable {
		t.Errorf("expected 503, got %d", rec.Code)
	}
}

func TestChatSSEWithQueryParam(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/chat/sse" {
			t.Errorf("expected path /api/v1/chat/sse, got %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "text/event-stream")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("data: {\"response\":\"ok\"}\n\n"))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewChatHandler(aiService.URL)
	router.GET("/api/v1/chat/sse", handler.ChatSSE)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/chat/sse?message=hello", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if rec.Header().Get("Content-Type") != "text/event-stream" {
		t.Errorf("expected Content-Type text/event-stream, got %s", rec.Header().Get("Content-Type"))
	}
	if !strings.Contains(rec.Body.String(), "ok") {
		t.Errorf("expected SSE body to contain 'ok', got: %s", rec.Body.String())
	}
}

func TestChatSSEWithPostBody(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var body map[string]any
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			t.Fatalf("failed to decode proxied body: %v", err)
		}
		if body["scenario"] != "route_plan" {
			t.Errorf("expected scenario to be preserved, got: %v", body["scenario"])
		}
		modelSettings, ok := body["model_settings"].(map[string]any)
		if !ok {
			t.Fatalf("expected model_settings to be preserved, got: %v", body["model_settings"])
		}
		llm, ok := modelSettings["llm"].(map[string]any)
		if !ok || llm["api_key"] != "runtime-key" {
			t.Fatalf("expected runtime llm api key to be preserved, got: %v", modelSettings["llm"])
		}
		w.Header().Set("Content-Type", "text/event-stream")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("data: ok\n\n"))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewChatHandler(aiService.URL)
	// ChatSSE is registered under POST for body-based calls
	router.POST("/api/v1/chat/sse", handler.ChatSSE)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/chat/sse",
		strings.NewReader(`{"message":"hello","chat_id":"chat-1","scenario":"route_plan","model_settings":{"llm":{"base_url":"https://runtime.example/v1","api_key":"runtime-key","model":"runtime-model"}}}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
}

func TestChatSSEMissingMessage(t *testing.T) {
	gin.SetMode(gin.TestMode)

	router := gin.New()
	handler := NewChatHandler("http://localhost:8000")
	router.GET("/api/v1/chat/sse", handler.ChatSSE)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/chat/sse", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusBadRequest {
		t.Errorf("expected 400, got %d", rec.Code)
	}
}

func TestChatHistoryProxiesToAIService(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		expectedPath := "/api/v1/chat/history/chat-123"
		if r.URL.Path != expectedPath {
			t.Errorf("expected path %s, got %s", expectedPath, r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"messages":[]}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewChatHandler(aiService.URL)
	router.GET("/api/v1/chat/history/:chatId", handler.ChatHistory)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/chat/history/chat-123", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "messages") {
		t.Errorf("expected response to contain messages, got: %s", rec.Body.String())
	}
}

func TestChatClearHistoryProxiesDeleteToAIService(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		expectedPath := "/api/v1/chat/history/chat-123"
		if r.URL.Path != expectedPath {
			t.Errorf("expected path %s, got %s", expectedPath, r.URL.Path)
		}
		if r.Method != http.MethodDelete {
			t.Errorf("expected DELETE, got %s", r.Method)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"chat_id":"chat-123","status":"cleared"}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewChatHandler(aiService.URL)
	router.DELETE("/api/v1/chat/history/:chatId", handler.ChatClearHistory)

	req := httptest.NewRequest(http.MethodDelete, "/api/v1/chat/history/chat-123", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "cleared") {
		t.Errorf("expected response to contain cleared, got: %s", rec.Body.String())
	}
}

func TestChatConfirmProxiesToAIService(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		expectedPath := "/api/v1/chat/confirm"
		if r.URL.Path != expectedPath {
			t.Errorf("expected path %s, got %s", expectedPath, r.URL.Path)
		}
		if r.Method != http.MethodPost {
			t.Errorf("expected POST, got %s", r.Method)
		}
		var body map[string]string
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			t.Fatalf("failed to decode proxied body: %v", err)
		}
		if body["confirmation_id"] != "confirm-1" || body["action"] != "confirm" {
			t.Errorf("unexpected proxied body: %v", body)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"status":"confirmed","confirmation_id":"confirm-1"}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewChatHandler(aiService.URL)
	router.POST("/api/v1/chat/confirm", handler.ChatConfirm)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/chat/confirm",
		strings.NewReader(`{"confirmation_id":"confirm-1","action":"confirm"}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "confirmed") {
		t.Errorf("expected response body to contain confirmed, got: %s", rec.Body.String())
	}
}

func TestChatPendingProxiesToAIService(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		expectedPath := "/api/v1/chat/pending/chat-123"
		if r.URL.Path != expectedPath {
			t.Errorf("expected path %s, got %s", expectedPath, r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"chat_id":"chat-123","pending":[]}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewChatHandler(aiService.URL)
	router.GET("/api/v1/chat/pending/:chatId", handler.ChatPending)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/chat/pending/chat-123", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "chat-123") {
		t.Errorf("expected response body to contain chat id, got: %s", rec.Body.String())
	}
}

func TestArtifactDownloadProxiesToAIService(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		expectedPath := "/api/v1/artifacts/reports/plan.pdf"
		if r.URL.Path != expectedPath {
			t.Errorf("expected path %s, got %s", expectedPath, r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/pdf")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("%PDF-1.4 demo"))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewChatHandler(aiService.URL)
	router.GET("/api/v1/artifacts/*filePath", handler.ArtifactDownload)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/artifacts/reports/plan.pdf", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if rec.Header().Get("Content-Type") != "application/pdf" {
		t.Errorf("expected application/pdf, got %s", rec.Header().Get("Content-Type"))
	}
	if rec.Body.String() != "%PDF-1.4 demo" {
		t.Errorf("unexpected body: %s", rec.Body.String())
	}
}

func TestChatHealthReturnsOk(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/api/v1/chat/health" {
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			_, _ = w.Write([]byte(`{"status":"ok"}`))
			return
		}
		http.NotFound(w, r)
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewChatHandler(aiService.URL)
	router.GET("/api/v1/chat/health", handler.ChatHealth)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/chat/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
}

func TestChatHealthFallsBackToGeneralHealth(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/api/v1/chat/health" {
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
	handler := NewChatHandler(aiService.URL)
	router.GET("/api/v1/chat/health", handler.ChatHealth)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/chat/health", nil)
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

func TestChatHealthBothEndpointsUnreachable(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/api/v1/chat/health" {
			w.WriteHeader(http.StatusNotFound)
			return
		}
		if r.URL.Path == "/health" {
			w.WriteHeader(http.StatusInternalServerError)
			_, _ = w.Write([]byte("db error"))
			return
		}
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewChatHandler(aiService.URL)
	router.GET("/api/v1/chat/health", handler.ChatHealth)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/chat/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusInternalServerError {
		t.Errorf("expected 500 when fallback also fails, got %d", rec.Code)
	}
}

func TestNewChatHandler(t *testing.T) {
	handler := NewChatHandler("http://test:8000")
	if handler == nil {
		t.Fatal("expected non-nil handler")
	}
}
