// TODO search by worker type, tags, and contractend
package main

import (
	"encoding/json"
	"log"
	"net/http"

	"./db"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	"github.com/go-chi/render"
)

func postWorker(w http.ResponseWriter, r *http.Request) {
	var worker db.Worker
	err := json.NewDecoder(r.Body).Decode(&worker)
	if err != nil {
		http.Error(w, http.StatusText(400), 400)
		log.Printf("error decoding body %+v: %+v", err, r.Body)
		return
	}

	result := db.CreateWorker(worker)

	if result.Error != nil {
		http.Error(w, http.StatusText(result.Code), result.Code)
		render.JSON(w, r, map[string]string{"error": result.Error.Error()})
		log.Printf("error creating worker: %+v", result.Error)
		return
	}

	render.JSON(w, r, map[string]string{"message": "OK"})
}

func putWorker(w http.ResponseWriter, r *http.Request) {
	var worker db.Worker
	err := json.NewDecoder(r.Body).Decode(&worker)
	if err != nil {
		http.Error(w, http.StatusText(400), 400)
		log.Printf("error decoding body %+v: %+v", err, r.Body)
		return
	}

	result := db.UpdateWorker(worker)

	if result.Error != nil {
		http.Error(w, http.StatusText(result.Code), result.Code)
		render.JSON(w, r, map[string]string{"error": result.Error.Error()})
		log.Printf("error updating worker: %+v", result.Error)
		return
	}

	render.JSON(w, r, map[string]string{"message": "OK"})
}

func getWorker(w http.ResponseWriter, r *http.Request) {
	email := chi.URLParam(r, "email")

	worker, result := db.ReadWorker(email)

	if result.Error != nil {
		http.Error(w, http.StatusText(result.Code), result.Code)
		render.JSON(w, r, map[string]string{"error": result.Error.Error()})
		log.Printf("error reading worker `%s`: %+v", email, result.Error)
		return
	}

	render.JSON(w, r, worker)
}

func deleteWorker(w http.ResponseWriter, r *http.Request) {
	email := chi.URLParam(r, "email")

	result := db.DeleteWorker(email)

	if result.Error != nil {
		http.Error(w, http.StatusText(result.Code), result.Code)
		render.JSON(w, r, map[string]string{"error": result.Error.Error()})
		log.Printf("error deleting worker `%s`: %+v", email, result.Error)
		return
	}

	render.JSON(w, r, map[string]string{"message": "OK"})
}

func main() {

	db.Init()
	defer db.Shutdown()

	r := chi.NewRouter()
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(render.SetContentType(render.ContentTypeJSON))

	r.Route("/worker", func(r chi.Router) {
		r.Post("/", postWorker)
		r.Put("/", putWorker)
		r.Delete("/{email}", deleteWorker)
		r.Get("/{email}", getWorker)
	})

	err := http.ListenAndServe(":80", r)

	if err != nil {
		log.Fatal("Failed to start the http server")
	}

}
