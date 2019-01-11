package main

import (
  "fmt"
  "runtime"
)

func main() {
	for i:=0; i<10; i++{
		raceIt()
	}
}

func googleIt(respond chan<- string, query string) {
  // Do stuff that causes latency
  fmt.Printf("Sent query: %s\n", query)
  respond <- query
}

func raceIt(){
  query1 := "Query1"
  query2 := "Query2"
  respond := make(chan string)

  go googleIt(respond, query1)
  go googleIt(respond, query2)
  queryResp := <-respond

  fmt.Printf("Number of CPUs: %d\n", runtime.NumCPU())
  fmt.Printf("Got Response: %s\n", queryResp)
}
