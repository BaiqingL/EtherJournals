package main

// https://gist.github.com/hongster/04660a20f2498fb7b680 Ok this works I guess

import(
  "net"
  "fmt"
  "bufio"
  "time"
)


func check(err error, message string) {

    if err != nil {
        panic(err)
    }
    fmt.Printf("%s\n", message)

}

func handleConnection(conn net.Conn){

  // Close connection when this function ends
  defer func() {
    fmt.Println("Closing connection.")
    conn.Close()
  }()

  timeoutDuration := 5 * time.Second
  buf := bufio.NewReader(conn)
    for{
      conn.SetReadDeadline(time.Now().Add(timeoutDuration))
      msg, err := buf.ReadString('\n')
      fmt.Printf("Data recieved: %v", msg)

      if string(msg) == "close\n"{
        fmt.Printf("Connection closed by host\n")
        conn.Write([]byte("goodbye.\n"))
        conn.Close()
      }

      if err != nil{
        fmt.Printf("\nConnection terminated.\n")
        conn.Close()
      }

      conn.Write([]byte("Connection recieved\n"))
    }
}



func main() {

  defer func() {
    ln.Close()
    fmt.Println("Listener closed")
  }()

  ln, err := net.Listen("tcp", ":8080")
  check(err, "Server Ready")

  for {

    conn, err := ln.Accept()

    check(err, "Connection established")

    go handleConnection(conn)
  }

}
