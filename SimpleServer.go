package main

import(
  "net";
  "fmt";
  "bufio";
  //"time";
)


// Make sure there is no secondary error, panic if otherwise
func check(err error, message string) {
    if err != nil {
        panic(err)
    }
    fmt.Printf("%s\n", message)
}


func main() {

  // Begin tcp server
  ln, err := net.Listen("tcp", ":8080")
  check(err, "Server Ready")

  // Forever loop to accept connections
  for {

    // Start to accept connections
    conn, err := ln.Accept()

    check(err, "Connection established")

    dataRecieved := make(chan bool, 1)

    // goroutine to process data from client
    go func(){

      //Read connection
      buf := bufio.NewReader(conn)


      // Keep connection alive
      for {
        msg, err := buf.ReadString('\n')

        fmt.Printf("Data recieved: %v", msg)
        go func(){
          dataRecieved <- true
        }()

        //fmt.Printf("%v\n", <- dataRecieved)

        // Mind the delim byte!
        if string(msg) == "close\n"{
          fmt.Printf("Connection closed by host\n")
          conn.Write([]byte("goodbye.\n"))
          conn.Close()
        }

        conn.Write([]byte("Connection recieved\n"))


        // If there is an error, terminate connection
        if err != nil{
          fmt.Printf("\nConnection terminated.\n")
          break
        }

      }
    }()
  }
}
