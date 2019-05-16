package main

import (
  "os"
  "fmt"
  "net"
  "time"
  "bufio"
  "keys"
)

func handleConnection(conn net.Conn) {
  fmt.Println("Handling new connection")

  // Close connection when this function ends
  defer func() {
    fmt.Println("Closing connection")
    conn.Close()
  }()

  // Enforce a timeout after 20 seconds of no response
  timeoutDuration := 20 * time.Second
  bufReader := bufio.NewReader(conn)

  // Print out where the connection is coming from
  fmt.Printf("New connection from %s\n",conn.RemoteAddr())

  for {
    // Set a deadline for reading. Read operation will fail if no data
    // is received after deadline.
    conn.SetReadDeadline(time.Now().Add(timeoutDuration))

    // Read tokens delimited by newline
    bytes, err := bufReader.ReadBytes('\n')
    if err != nil {
      fmt.Println(err)
      return
    }

    switch{
    case string(bytes) == "close\n":
      conn.Write([]byte("Closing connection\n"))
      conn.Close()
    case string(bytes) == "help\n":
      conn.Write([]byte("Current commands:\nClose\nHelp\n"))
    default:
      // Encrypt and yeet
      conn.Write([]byte(keys.EncryptData(bytes)))
    }
    // Show what the server recieved
    fmt.Printf("%s", bytes)
  }
}



func main() {

  // Importing the keys
  if _, err := os.Stat("privkey.pem"); os.IsNotExist(err) {
    fmt.Println("Private key not found, generating...")
    keys.GeneratePrivKey()
  } else {
    fmt.Println("Private key found")
    privkey := keys.ImportPrivKey()
    fmt.Println(privkey)
  }

  // Start listening to port 8080 for TCP connections
  listener, err:= net.Listen("tcp", ":8080")
  if err != nil {
    fmt.Println(err)
    return
  }

  defer func() {
    listener.Close()
    fmt.Println("Listener closed")
  }()

  for {
    // Get net.TCPConn object
    conn, err := listener.Accept()
    if err != nil {
      fmt.Println(err)
      break
    }

    //Allow go to handle multiple connections
    go handleConnection(conn)

  }
}
