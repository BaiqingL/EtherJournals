package main

/* TODO
Read files into bytes
Compress said bytes
Upload to IPFS with option to pin
Profit?
*/


import (
    "strings"
    "os"
    "fmt"
    shell "github.com/ipfs/go-ipfs-api"
)

func main() {
        writeToIPFS("ipfs api in golang")
}


func writeToIPFS(alphaContent string){
        // Where your local node is running on localhost:5001
        sh := shell.NewShell("localhost:5001")
        cid, err := sh.Add(strings.NewReader(alphaContent))
        if err != nil {
        fmt.Fprintf(os.Stderr, "error: %s", err)
        os.Exit(1)
        }
    fmt.Printf("added %s\n", cid)
}
