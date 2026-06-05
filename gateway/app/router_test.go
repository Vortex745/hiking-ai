package app

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/ai-hiking/gateway/config"
)

func TestRouterMountsToolsHealth(t *testing.T) {
	aiService := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/tools/health" {
			t.Errorf("expected path /api/v1/tools/health, got %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"status":"ok","module":"tools"}`))
	}))
	defer aiService.Close()

	router := NewRouter(&config.Config{
		Port:           "0",
		AIServiceURL:   aiService.URL,
		AllowedOrigins: "*",
	})

	req := httptest.NewRequest(http.MethodGet, "/api/v1/tools/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), `"module":"tools"`) {
		t.Errorf("expected tools health body, got: %s", rec.Body.String())
	}
}
