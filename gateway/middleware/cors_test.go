package middleware

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestCORSMiddlewareParsesMultipleOrigins(t *testing.T) {
	gin.SetMode(gin.TestMode)

	handler := CORSMiddleware("http://a.com, http://b.com")

	router := gin.New()
	router.Use(handler)
	router.GET("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"ok": true})
	})

	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	req.Header.Set("Origin", "http://a.com")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Header().Get("Access-Control-Allow-Origin") != "http://a.com" {
		t.Errorf("expected CORS origin header http://a.com, got: %s", rec.Header().Get("Access-Control-Allow-Origin"))
	}
}

func TestCORSMiddlewareEmptyOriginsRejects(t *testing.T) {
	gin.SetMode(gin.TestMode)

	handler := CORSMiddleware("")

	router := gin.New()
	router.Use(handler)
	router.GET("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"ok": true})
	})

	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	req.Header.Set("Origin", "http://evil.com")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusForbidden {
		t.Errorf("empty origin list should reject with 403, got: %d", rec.Code)
	}
}

func TestCORSMiddlewarePreflight(t *testing.T) {
	gin.SetMode(gin.TestMode)

	handler := CORSMiddleware("http://localhost:5173")

	router := gin.New()
	router.Use(handler)
	router.OPTIONS("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"ok": true})
	})

	req := httptest.NewRequest(http.MethodOptions, "/test", nil)
	req.Header.Set("Origin", "http://localhost:5173")
	req.Header.Set("Access-Control-Request-Method", "POST")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Header().Get("Access-Control-Allow-Origin") != "http://localhost:5173" {
		t.Errorf("expected CORS on preflight, got: %s", rec.Header().Get("Access-Control-Allow-Origin"))
	}
	if rec.Header().Get("Access-Control-Allow-Credentials") != "true" {
		t.Errorf("expected AllowCredentials=true, got: %s", rec.Header().Get("Access-Control-Allow-Credentials"))
	}
}

func TestCORSMiddlewareAllowedMethods(t *testing.T) {
	gin.SetMode(gin.TestMode)

	handler := CORSMiddleware("http://localhost:5173")

	router := gin.New()
	router.Use(handler)
	router.OPTIONS("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"ok": true})
	})

	req := httptest.NewRequest(http.MethodOptions, "/test", nil)
	req.Header.Set("Origin", "http://localhost:5173")
	req.Header.Set("Access-Control-Request-Method", "POST")
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	methods := rec.Header().Get("Access-Control-Allow-Methods")
	if methods == "" {
		t.Error("expected Access-Control-Allow-Methods header on OPTIONS preflight request")
	}
}
