package db

import (
	"context"
	"errors"
	"log"
	"os"
	"time"

	"github.com/mongodb/mongo-go-driver/bson"
	"github.com/mongodb/mongo-go-driver/mongo"
)

var client *mongo.Client
var workersCollection *mongo.Collection

type DbOpResult struct {
	Code  int
	Error error
}

type Worker struct {
	Email        string   `json:"email" bson:"_id"`
	Name         string   `json:"name" bson:"name"`
	IsContractor bool     `json:"isContractor" bson:"isContractor"`
	ContractEnd  string   `json:"contractEnd,omitempty" bson:"contractEnd,omitempty"`
	JobTitle     string   `json:"jobTitle,omitempty" bson:"jobTitle,omitempty"`
	Tags         []string `json:"tags" bson:"tags"`
}

func Init() {

	mongoAddr := os.Getenv("MONGO_ADDRESS")
	var err error

	for i := 0; i < 3; i++ {
		client, err = mongo.NewClient(mongoAddr)
		if err == nil {
			break
		}
		time.Sleep(1000 * time.Millisecond)
	}
	if err != nil {
		log.Fatal("Failed to connect to the database at", mongoAddr)
	}

	err = client.Connect(context.Background())
	if err != nil {
		log.Fatal("Failed to connect to the database")
	}
	workersCollection = client.Database("team").Collection("workers")
}

func Shutdown() {
	client.Disconnect(nil)
}

func validateWorker(worker Worker) (bool, string) {
	if len(worker.Email) == 0 {
        return false, "an email is required"
    }

    if worker.IsContractor {
		_, err := time.Parse(
			time.RFC3339,
			worker.ContractEnd)
		if err != nil {
			return false, "invalid contract end date for a contractor, must be in RFC3339"
		}
	}

	if !worker.IsContractor && len(worker.JobTitle) == 0 {
		return false, "a job title is required for employees"
	}

	if !worker.IsContractor && len(worker.ContractEnd) > 0 {
		return false, "no contract end date for employees"
	}

	if worker.IsContractor && len(worker.JobTitle) > 0 {
		return false, "no job titles for contractors"
	}

	return true, ""
}

func CreateWorker(worker Worker) DbOpResult {

	valid, msg := validateWorker(worker)

	if !valid {
		return DbOpResult{400, errors.New(msg)}
	}

	_, err := workersCollection.InsertOne(context.Background(), worker)
	if err != nil {
		return DbOpResult{500, err}
	}

	return DbOpResult{200, nil}
}

func UpdateWorker(worker Worker) DbOpResult {

	valid, msg := validateWorker(worker)

	if !valid {
		return DbOpResult{400, errors.New(msg)}
	}

	_, err := workersCollection.UpdateOne(
		context.Background(),
		bson.D{{"_id", worker.Email}},
		bson.D{{"$set", worker}},
	)
	if err != nil {
		return DbOpResult{500, err}
	}

	return DbOpResult{200, nil}
}

func DeleteWorker(email string) DbOpResult {

	_, err := workersCollection.DeleteOne(context.Background(), bson.M{"_id": email})
	if err != nil {
		return DbOpResult{500, err}
	}
	return DbOpResult{200, nil}
}

func ReadWorker(email string) (Worker, DbOpResult) {

	var worker Worker
	result := workersCollection.FindOne(context.Background(), bson.M{"_id": email})
	if result.Err() != nil {
		return worker, DbOpResult{500, result.Err()}
	}
	err := result.Decode(&worker)
	if err != nil {
		return worker, DbOpResult{404, err}
	}

	return worker, DbOpResult{200, nil}
}
