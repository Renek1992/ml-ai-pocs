package main

import (
	"log"
	"net/http"
	"poc__llm_sql_builder/internal/routes"
)

func main() {
	router := routes.SetupRoutes()
	log.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", router); err != nil {
		log.Fatal(err)
	}
}
