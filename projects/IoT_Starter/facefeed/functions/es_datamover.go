// Copyright (c) 2018 Nutanix, Inc.
// Use of this source code is governed by an MIT-style license 
// found in the LICENSE file at https://github.com/nutanix/xi-iot.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	elastic "gopkg.in/olivere/elastic.v5"
	nuruntime "nutanix.com/sherlock/runtime"
)

const (
	esEndpoint = "http://elasticsearch:9200" // We assume ES svc already exists in project ns
)

var (
	//output topic
	esIndex = "datastream-faceregister" // Overwritten by config variable
)

const mapping = `
{
	"settings":{
		"number_of_shards": 1,
		"number_of_replicas": 0
	},
	"mappings":{
		"message":{
			"properties":{
				"SherlockTimestamp":{
					"type":"date",
					"format": "epoch_millis"
				}
			}
		}
	}
}`

type ElasticDataMover struct {
	client *elastic.Client
	ctx    context.Context
}

var elasticDataMover *ElasticDataMover

func NewElasticDataMover(
	client *elastic.Client,
	ctx context.Context) *ElasticDataMover {

	return &ElasticDataMover{
		client: client,
		ctx:    ctx,
	}
}

func PushDataToES(ctx *nuruntime.Context, bytes []byte) error {
	esIndex = ctx.GetConfig()["esIndex"]
	if err := sendToES(bytes); err != nil {
		return err // Don't send to NATS
	}
	ctx.Send(bytes) // required by facefeed application
	return nil
}

func sendToES(bytes []byte) error {
	jsonMsg := DataStreamMsg2Json(bytes)
	put, err := elasticDataMover.client.Index().
		Index(esIndex).
		Type("message").
		Id(fmt.Sprintf("%d", getMillisecTimestamp())).
		BodyString(string(jsonMsg)).
		Do(elasticDataMover.ctx)
	if err != nil {
		log.Printf("Failed to put message '%s': %s",
			jsonMsg, err)
		return err
	}
	log.Printf("Published to ElasticSearch index '%s' Id=%s",
		put.Index, put.Id)
	return nil
}

// DataStreamMsg2Json Code from outputdriver.go (lot of it)
func DataStreamMsg2Json(p []byte) []byte {
	// treat message as bag of key-val pairs
	payload := make(map[string]*json.RawMessage)
	// non-json payload to be added as binary
	if err := json.Unmarshal(p, &payload); err != nil {
		p, err := json.Marshal(p)
		if err != nil {
			// should never happen
			panic(fmt.Sprintf("Failed to marshal payload: %s", err))
		}
		payload["Payload"] = (*json.RawMessage)(&p)
	}
	// add timestamp in milliseconds as new field to message
	timeMillis := getMillisecTimestamp()
	timestamp, err := json.Marshal(timeMillis)
	if err != nil {
		// should never happen
		panic(fmt.Sprintf("Failed to marshal timestamp: %s", err))
	}
	payload["SherlockTimestamp"] = (*json.RawMessage)(&timestamp)
	// convert back to JSON after adding timestamp
	b, err := json.Marshal(payload)
	if err != nil {
		// should never happen
		panic(fmt.Sprintf("Failed to marshal payload: %s", err))
	}
	log.Printf("JSON Message: %s", string(b))
	return b
}

func getMillisecTimestamp() int64 {
	return time.Now().UnixNano() / int64(time.Millisecond)
}

func main() {
	// RFC We are logging before flag.Parse
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	log.Printf("Connecting to %s", esEndpoint)
	client, err := elastic.NewClient(elastic.SetURL(esEndpoint))
	if err != nil {
		log.Fatalf("Connecting to ElasticSearch failed: %s", err)
	}
	defer client.Stop()

	info, code, err := client.Ping(esEndpoint).Do(ctx)
	if err != nil {
		log.Fatalf("Ping to ElasticSearch failed: %s", err)
	}
	log.Printf("ES Info: %+v, Code: %d", *info, code)

	// Pre create indices if already don't exist
	createESIndex(client, ctx, "datastream-faceregister")
	createESIndex(client, ctx, "datastream-facerecognitionlivefeed")

	elasticDataMover =
		NewElasticDataMover(client, ctx)

	log.Printf("Starting Elastic DataMover")

	// Start processing messages
	nuruntime.Start(PushDataToES)
}

func createESIndex(client *elastic.Client, ctx context.Context, index string) {
	exists, err := client.IndexExists(index).Do(ctx)
	if err != nil {
		log.Fatalf("Failed to look up index '%s': %v",
			index, err)
	}
	if exists {
		log.Printf("Index '%s' exists already", index)
	} else {
		log.Printf("Create index '%s'", index)
		createIndex, err := client.CreateIndex(index).
			BodyString(mapping).Do(ctx)
		if err != nil {
			log.Fatalf("FailedStart to create index '%s': %v",
				index, err)
		}
		if !createIndex.Acknowledged {
			log.Printf("Index not acknowledged '%s': %v",
				index, err)
		}
	}
}
