package handler

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestHealthHandlerReturnsOk(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"status":"ok"}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewHealthHandler(aiService.URL)
	router.GET("/health", handler.Health)

	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}

	var body map[string]string
	if err := json.Unmarshal(rec.Body.Bytes(), &body); err != nil {
		t.Fatalf("failed to parse JSON: %v", err)
	}

	if body["status"] != "ok" {
		t.Errorf("expected status 'ok', got '%s'", body["status"])
	}
	if body["service"] != "gateway" {
		t.Errorf("expected service 'gateway', got '%s'", body["service"])
	}
	if body["ai_service"] != "ok" {
		t.Errorf("expected ai_service 'ok', got '%s'", body["ai_service"])
	}
}

func TestHealthHandlerAIUnreachable(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// Start a server that will be closed immediately
	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	aiService.Close()

	handler := NewHealthHandler(aiService.URL)

	router := gin.New()
	router.GET("/health", handler.Health)

	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("gateway should still report ok, got %d", rec.Code)
	}

	var body map[string]string
	if err := json.Unmarshal(rec.Body.Bytes(), &body); err != nil {
		t.Fatalf("failed to parse JSON: %v", err)
	}

	if body["status"] != "ok" {
		t.Errorf("expected gateway status 'ok', got '%s'", body["status"])
	}
	if body["ai_service"] != "unreachable" {
		t.Errorf("expected ai_service 'unreachable', got '%s'", body["ai_service"])
	}
}

func TestHealthHandlerAIError(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = w.Write([]byte("internal error"))
	}))
	defer aiService.Close()

	handler := NewHealthHandler(aiService.URL)

	router := gin.New()
	router.GET("/health", handler.Health)

	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("gateway should still report ok, got %d", rec.Code)
	}

	var body map[string]string
	if err := json.Unmarshal(rec.Body.Bytes(), &body); err != nil {
		t.Fatalf("failed to parse JSON: %v", err)
	}

	if body["ai_service"] != "error: internal error" {
		t.Errorf("expected ai_service error message, got '%s'", body["ai_service"])
	}
}

func TestNewHealthHandler(t *testing.T) {
	gin.SetMode(gin.TestMode)

	handler := NewHealthHandler("http://test:8000")
	if handler == nil {
		t.Fatal("expected non-nil handler")
	}
	if handler.aiServiceURL != "http://test:8000" {
		t.Errorf("expected aiServiceURL 'http://test:8000', got '%s'", handler.aiServiceURL)
	}
}
