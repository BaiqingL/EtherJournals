package main

import (
    "fmt"
    "sync"
    "time"
)

func dosomething(millisecs time.Duration, wg *sync.WaitGroup) {
    duration := millisecs * time.Millisecond
    time.Sleep(duration) // Sleeps the duration specified in ms
    fmt.Println("Function in background, duration:", duration)
    wg.Done()
}

func main() {
    var wg sync.WaitGroup // Create the workgroup to wait

    // You would want to add a workgroup every time before actually needing it
    wg.Add(1)
    go dosomething(200, &wg)

    wg.Add(1)
    go dosomething(400, &wg)

    wg.Add(1)
    go dosomething(1500, &wg)

    wg.Add(1)
    go dosomething(150, &wg)

    wg.Add(1)
    go dosomething(600, &wg)

    wg.Wait()
    fmt.Println("Done")
}
