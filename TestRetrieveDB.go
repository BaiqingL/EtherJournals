package main

import (
	"fmt"
	"github.com/syndtr/goleveldb/leveldb"
	"log"
)

func main() {

	db, err := leveldb.OpenFile("test.db", nil)
	if err != nil {
		log.Fatal("Yikes!")
	}
	defer db.Close()
	fmt.Println("Database opened")
	
	data, err := db.Get([]byte("450000"), nil)
	fmt.Printf("%s", data)
}
