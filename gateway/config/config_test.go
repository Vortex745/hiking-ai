package config

import (
	"os"
	"testing"
)

func TestLoadDefaults(t *testing.T) {
	_ = os.Unsetenv("PORT")
	_ = os.Unsetenv("AI_SERVICE_URL")
	_ = os.Unsetenv("ALLOWED_ORIGINS")

	cfg := Load()
	if cfg.Port != "8080" {
		t.Errorf("expected default port 8080, got %s", cfg.Port)
	}
	if cfg.AIServiceURL != "http://localhost:8000" {
		t.Errorf("expected default AI service URL http://localhost:8000, got %s", cfg.AIServiceURL)
	}
	if cfg.AllowedOrigins != "http://localhost:5173,http://127.0.0.1:5173" {
		t.Errorf("unexpected allowed origins: %s", cfg.AllowedOrigins)
	}
}

func TestLoadFromEnv(t *testing.T) {
	t.Setenv("PORT", "9090")
	t.Setenv("AI_SERVICE_URL", "http://ai:9000")
	t.Setenv("ALLOWED_ORIGINS", "*")

	cfg := Load()
	if cfg.Port != "9090" {
		t.Errorf("expected port 9090, got %s", cfg.Port)
	}
	if cfg.AIServiceURL != "http://ai:9000" {
		t.Errorf("expected AI service URL http://ai:9000, got %s", cfg.AIServiceURL)
	}
	if cfg.AllowedOrigins != "*" {
		t.Errorf("expected allowed origins *, got %s", cfg.AllowedOrigins)
	}
}

func TestGetEnvWithFallback(t *testing.T) {
	_ = os.Unsetenv("TEST_GETENV_FALLBACK")
	result := getEnv("TEST_GETENV_FALLBACK", "fallback")
	if result != "fallback" {
		t.Errorf("expected fallback, got %s", result)
	}
}

func TestGetEnvWithValue(t *testing.T) {
	t.Setenv("TEST_GETENV_VALUE", "value")
	result := getEnv("TEST_GETENV_VALUE", "fallback")
	if result != "value" {
		t.Errorf("expected 'value', got %s", result)
	}
}

func TestGetEnvEmptyValueUsesFallback(t *testing.T) {
	t.Setenv("TEST_GETENV_EMPTY", "")
	result := getEnv("TEST_GETENV_EMPTY", "fallback")
	if result != "fallback" {
		t.Errorf("expected fallback when env is empty, got %s", result)
	}
}
