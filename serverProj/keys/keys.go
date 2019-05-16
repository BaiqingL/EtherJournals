package keys

import (
  "crypto/rand"
  "crypto/rsa"
  "crypto/x509"
  "encoding/pem"
  "os"
  "fmt"
  "bufio"
)

func GeneratePrivKey(){

  privKey, err := rsa.GenerateKey(rand.Reader, 4096)
  if err != nil {
      fmt.Println(err.Error)
      os.Exit(1)
  }

  pemPrivFile, err := os.Create("privkey.pem")
  if err != nil {
      fmt.Println(err)
      os.Exit(1)
  }

  var pemPrivBlock = &pem.Block{
    Type:  "RSA PRIVATE KEY",
    Bytes: x509.MarshalPKCS1PrivateKey(privKey),
  }

  err = pem.Encode(pemPrivFile, pemPrivBlock)
  if err != nil {
      fmt.Println(err)
      os.Exit(1)
  }
  pemPrivFile.Close()
}

func ImportPrivKey() (*rsa.PrivateKey){
  privKeyFile, err := os.Open("privkey.pem")
  if err != nil {
    fmt.Println(err)
    os.Exit(1)
  }
  pemfileinfo, _ := privKeyFile.Stat()
  var size int64 = pemfileinfo.Size()
  pembytes := make([]byte, size)
  buffer := bufio.NewReader(privKeyFile)
  _, err = buffer.Read(pembytes)
  data, _ := pem.Decode([]byte(pembytes))
  privKeyFile.Close()

  privKeyImported, err := x509.ParsePKCS1PrivateKey(data.Bytes)
  if err != nil {
    fmt.Println(err)
    os.Exit(1)
  }
  return privKeyImported
}
