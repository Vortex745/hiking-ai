package handler

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestToolsHealthReturnsOk(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/tools/health" {
			t.Errorf("expected path /api/v1/tools/health, got %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"status":"ok","mcp":{"configured":true}}`))
	}))
	defer aiService.Close()

	router := gin.New()
	handler := NewToolsHandler(aiService.URL)
	router.GET("/api/v1/tools/health", handler.ToolsHealth)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/tools/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), `"mcp"`) {
		t.Errorf("expected proxied tools health body, got: %s", rec.Body.String())
	}
}

func TestToolsHealthFallsBackToGeneralHealth(t *testing.T) {
	gin.SetMode(gin.TestMode)

	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/api/v1/tools/health" {
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
	handler := NewToolsHandler(aiService.URL)
	router.GET("/api/v1/tools/health", handler.ToolsHealth)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/tools/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}

	var body map[string]string
	if err := json.Unmarshal(rec.Body.Bytes(), &body); err != nil {
		t.Fatalf("failed to parse JSON: %v", err)
	}
	if body["module"] != "tools" || body["fallback"] != "ai-service-health" {
		t.Errorf("expected tools fallback response, got: %v", body)
	}
}
