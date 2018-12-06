package main
// Test LevelDB performance

import (
	"fmt"
	"github.com/syndtr/goleveldb/leveldb"
	"log"
	"strconv"
)

func main() {

	db, err := leveldb.OpenFile("test.db", nil)
	if err != nil {
		log.Fatal("Yikes!")
	}
	defer db.Close()
	fmt.Println("Database opened")

	// 500k entries test
	for i := 0; i < 500000; i++ {
		err = db.Put([]byte(strconv.Itoa(i)), []byte("database data: "+strconv.Itoa(i)), nil)
	}
	

	iter := db.NewIterator(nil, nil)
	for iter.Next() {
		key := iter.Key()
		value := iter.Value()
		// First key then value
		fmt.Printf("%s %s\n", key, value)
	}

	iter.Release()
	err = iter.Error()
}
