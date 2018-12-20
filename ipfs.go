package main

/* TODO:
Allow user to specify files
Pin files
Profit?
*/

import (
	"bytes"
	"fmt"
	"github.com/ipfs/go-ipfs-api"
	"io/ioutil"
	"os"
)

func main() {
	file := readFile("example.pdf")
	writeToIPFS(file)
}

func readFile(filename string) []byte{
	bytes, err:= ioutil.ReadFile(filename)
	if err != nil {
		fmt.Print(err)
	}
	return bytes
}

func writeToIPFS(alphaContent []byte){
	sh := shell.NewShell("localhost:5001")
	id, err := sh.Add(bytes.NewReader(alphaContent))
	if err != nil {
        fmt.Fprintf(os.Stderr, "error: %s", err)
        os.Exit(1)
	}
    fmt.Printf("IPFS hash: %s\n", id)
}
