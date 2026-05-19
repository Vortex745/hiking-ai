package handler

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestModelsFetchSuccess(t *testing.T) {
	gin.SetMode(gin.TestMode)

	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/models" {
			t.Errorf("expected path /models, got %s", r.URL.Path)
		}
		if r.Header.Get("Authorization") != "Bearer test-key" {
			t.Errorf("expected Bearer token, got: %s", r.Header.Get("Authorization"))
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"data":[{"id":"gpt-4"}]}`))
	}))
	defer upstream.Close()

	router := gin.New()
	handler := NewModelsHandler("http://placeholder")
	router.POST("/api/v1/models/fetch", handler.ModelsFetch)

	body := `{"base_url":"` + upstream.URL + `","api_key":"test-key"}`
	req := httptest.NewRequest(http.MethodPost, "/api/v1/models/fetch",
		strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "gpt-4") {
		t.Errorf("expected response to contain gpt-4, got: %s", rec.Body.String())
	}
}

func TestModelsFetchMissingBaseURL(t *testing.T) {
	gin.SetMode(gin.TestMode)

	router := gin.New()
	handler := NewModelsHandler("http://placeholder")
	router.POST("/api/v1/models/fetch", handler.ModelsFetch)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/models/fetch",
		strings.NewReader(`{"api_key":"test-key"}`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusBadRequest {
		t.Errorf("expected 400, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "base_url is required") {
		t.Errorf("expected error about base_url, got: %s", rec.Body.String())
	}
}

func TestModelsFetchInvalidBody(t *testing.T) {
	gin.SetMode(gin.TestMode)

	router := gin.New()
	handler := NewModelsHandler("http://placeholder")
	router.POST("/api/v1/models/fetch", handler.ModelsFetch)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/models/fetch",
		strings.NewReader(`not json`))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusBadRequest {
		t.Errorf("expected 400 for invalid JSON, got %d", rec.Code)
	}
}

func TestModelsFetchUpstreamUnreachable(t *testing.T) {
	gin.SetMode(gin.TestMode)

	router := gin.New()
	handler := NewModelsHandler("http://placeholder")
	router.POST("/api/v1/models/fetch", handler.ModelsFetch)

	body := `{"base_url":"http://127.0.0.1:1","api_key":"key"}`
	req := httptest.NewRequest(http.MethodPost, "/api/v1/models/fetch",
		strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusServiceUnavailable {
		t.Errorf("expected 503, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "upstream unreachable") {
		t.Errorf("expected upstream unreachable error, got: %s", rec.Body.String())
	}
}

func TestModelsFetchUpstreamError(t *testing.T) {
	gin.SetMode(gin.TestMode)

	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusUnauthorized)
		_, _ = w.Write([]byte(`{"error":"invalid api key"}`))
	}))
	defer upstream.Close()

	router := gin.New()
	handler := NewModelsHandler("http://placeholder")
	router.POST("/api/v1/models/fetch", handler.ModelsFetch)

	body := `{"base_url":"` + upstream.URL + `","api_key":"bad-key"}`
	req := httptest.NewRequest(http.MethodPost, "/api/v1/models/fetch",
		strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusUnauthorized {
		t.Errorf("expected 401, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "invalid api key") {
		t.Errorf("expected error message from upstream, got: %s", rec.Body.String())
	}
}

func TestNewModelsHandler(t *testing.T) {
	handler := NewModelsHandler("http://test:8000")
	if handler == nil {
		t.Fatal("expected non-nil handler")
	}
}
