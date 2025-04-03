package routes

import (
	"net/http"
	"poc__llm_sql_builder/internal/handlers"

	"github.com/gorilla/mux"
)

func SetupRoutes(r *mux.Router, h *handlers.Handler) {
	r.HandleFunc("/items", h.GetItems).Methods(http.MethodGet)
	r.HandleFunc("/items", h.CreateItem).Methods(http.MethodPost)
}
