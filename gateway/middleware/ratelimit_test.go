package middleware

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
)

func TestRateLimitAllowsWithinLimit(t *testing.T) {
	gin.SetMode(gin.TestMode)

	handler := RateLimitMiddleware(10, time.Second)

	router := gin.New()
	router.Use(handler)
	router.GET("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"ok": true})
	})

	for i := 0; i < 10; i++ {
		req := httptest.NewRequest(http.MethodGet, "/test", nil)
		rec := httptest.NewRecorder()
		router.ServeHTTP(rec, req)
		if rec.Code != http.StatusOK {
			t.Fatalf("request %d should be allowed, got status %d", i+1, rec.Code)
		}
	}
}

func TestRateLimitBlocksExcess(t *testing.T) {
	gin.SetMode(gin.TestMode)

	handler := RateLimitMiddleware(5, time.Minute)

	router := gin.New()
	router.Use(handler)
	router.GET("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"ok": true})
	})

	// Use up all 5 tokens
	for i := 0; i < 5; i++ {
		req := httptest.NewRequest(http.MethodGet, "/test", nil)
		rec := httptest.NewRecorder()
		router.ServeHTTP(rec, req)
		if rec.Code != http.StatusOK {
			t.Fatalf("request %d should be allowed, got status %d", i+1, rec.Code)
		}
	}

	// 6th request should be rate limited
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)
	if rec.Code != http.StatusTooManyRequests {
		t.Errorf("expected 429 Too Many Requests, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "rate limit exceeded") {
		t.Errorf("expected 'rate limit exceeded' message, got: %s", rec.Body.String())
	}
}

func TestRateLimitTokensRefill(t *testing.T) {
	gin.SetMode(gin.TestMode)

	// rate=1 per 50ms means refill happens quickly
	handler := RateLimitMiddleware(1, 50*time.Millisecond)

	router := gin.New()
	router.Use(handler)
	router.GET("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"ok": true})
	})

	// Consume the single token
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("first request should be allowed, got %d", rec.Code)
	}

	// Wait for refill
	time.Sleep(60 * time.Millisecond)

	// Should be allowed again after refill
	req = httptest.NewRequest(http.MethodGet, "/test", nil)
	rec = httptest.NewRecorder()
	router.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Errorf("after refill, request should be allowed, got %d", rec.Code)
	}
}

func TestRateLimitPerIPTracking(t *testing.T) {
	gin.SetMode(gin.TestMode)

	handler := RateLimitMiddleware(1, time.Minute)

	router := gin.New()
	router.Use(handler)
	router.GET("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"ok": true})
	})

	// Request from IP-A consumes its token
	reqA := httptest.NewRequest(http.MethodGet, "/test", nil)
	reqA.RemoteAddr = "192.168.1.1:12345"
	recA := httptest.NewRecorder()
	router.ServeHTTP(recA, reqA)
	if recA.Code != http.StatusOK {
		t.Fatalf("IP-A first request allowed, got %d", recA.Code)
	}

	// Request from IP-B is a different bucket
	reqB := httptest.NewRequest(http.MethodGet, "/test", nil)
	reqB.RemoteAddr = "192.168.1.2:12345"
	recB := httptest.NewRecorder()
	router.ServeHTTP(recB, reqB)
	if recB.Code != http.StatusOK {
		t.Errorf("IP-B first request should be allowed (different bucket), got %d", recB.Code)
	}

	// IP-A second request should be blocked
	reqA2 := httptest.NewRequest(http.MethodGet, "/test", nil)
	reqA2.RemoteAddr = "192.168.1.1:12345"
	recA2 := httptest.NewRecorder()
	router.ServeHTTP(recA2, reqA2)
	if recA2.Code != http.StatusTooManyRequests {
		t.Errorf("IP-A second request should be rate limited, got %d", recA2.Code)
	}
}
