package main

import (
	"fmt"
	"time"

	"github.com/gin-gonic/gin"

	"github.com/ai-hiking/gateway/config"
	"github.com/ai-hiking/gateway/handler"
	"github.com/ai-hiking/gateway/middleware"
)

func main() {
	cfg := config.Load()

	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	// Global middleware
	r.Use(middleware.CORSMiddleware(cfg.AllowedOrigins))
	r.Use(middleware.RateLimitMiddleware(60, 1*time.Minute))

	// Handlers
	healthHandler := handler.NewHealthHandler(cfg.AIServiceURL)
	chatHandler := handler.NewChatHandler(cfg.AIServiceURL)
	modelsHandler := handler.NewModelsHandler(cfg.AIServiceURL)
	ragHandler := handler.NewRAGHandler(cfg.AIServiceURL)

	// Routes
	r.GET("/health", healthHandler.Health)

	api := r.Group("/api/v1")
	{
		api.GET("/chat/health", chatHandler.ChatHealth)
		api.POST("/chat/sync", chatHandler.ChatSync)
		api.POST("/chat/sse", chatHandler.ChatSSE)
		api.GET("/chat/history/:chatId", chatHandler.ChatHistory)

		api.POST("/models/fetch", modelsHandler.ModelsFetch)

		api.GET("/rag/health", ragHandler.RagHealth)
		api.POST("/rag/upload", ragHandler.RagUpload)
		api.POST("/rag/query", ragHandler.RagQuery)
		api.GET("/rag/documents", ragHandler.RagDocuments)
		api.POST("/rag/feishu/sync", ragHandler.FeishuSync)
		api.POST("/rag/feishu/default-sync", ragHandler.FeishuDefaultSync)
	}

	addr := fmt.Sprintf(":%s", cfg.Port)
	fmt.Printf("Gateway starting on %s\n", addr)
	fmt.Printf("AI Service URL: %s\n", cfg.AIServiceURL)
	fmt.Printf("Allowed Origins: %s\n", cfg.AllowedOrigins)

	if err := r.Run(addr); err != nil {
		panic(fmt.Sprintf("Failed to start server: %v", err))
	}
}
