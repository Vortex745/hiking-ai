package config

import "os"

// Config holds the gateway configuration.
type Config struct {
	Port           string
	AIServiceURL   string
	AllowedOrigins string
}

// Load reads configuration from environment variables.
func Load() *Config {
	return &Config{
		Port:           getEnv("PORT", "8080"),
		AIServiceURL:   getEnv("AI_SERVICE_URL", "http://localhost:8000"),
		AllowedOrigins: getEnv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"),
	}
}

func getEnv(key, fallback string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return fallback
}
