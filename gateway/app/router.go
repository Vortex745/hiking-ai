package app

import (
	"time"

	"github.com/gin-gonic/gin"

	"github.com/ai-hiking/gateway/config"
	"github.com/ai-hiking/gateway/handler"
	"github.com/ai-hiking/gateway/middleware"
)

// NewRouter builds the gateway HTTP router for both local servers and Vercel Functions.
func NewRouter(cfg *config.Config) *gin.Engine {
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	r.Use(middleware.CORSMiddleware(cfg.AllowedOrigins))
	r.Use(middleware.RateLimitMiddleware(60, 1*time.Minute))

	healthHandler := handler.NewHealthHandler(cfg.AIServiceURL)
	chatHandler := handler.NewChatHandler(cfg.AIServiceURL)
	modelsHandler := handler.NewModelsHandler(cfg.AIServiceURL)
	ragHandler := handler.NewRAGHandler(cfg.AIServiceURL)

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
		api.GET("/rag/history/:chatId", ragHandler.RagHistory)
		api.DELETE("/rag/history/:chatId", ragHandler.RagClearHistory)
	}

	return r
}
