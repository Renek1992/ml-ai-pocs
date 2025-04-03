package handlers

import (
	"encoding/json"
	"net/http"
	"sync"
)

type Item struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type Handler struct {
	mu    sync.Mutex
	items []Item
}

func NewHandler() *Handler {
	return &Handler{
		items: []Item{},
	}
}

func (h *Handler) GetItems(w http.ResponseWriter, r *http.Request) {
	h.mu.Lock()
	defer h.mu.Unlock()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(h.items)
}

func (h *Handler) CreateItem(w http.ResponseWriter, r *http.Request) {
	var item Item
	if err := json.NewDecoder(r.Body).Decode(&item); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	h.mu.Lock()
	h.items = append(h.items, item)
	h.mu.Unlock()
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(item)
}
