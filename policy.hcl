path "secret/data/gmail/*" {
  capabilities = ["read"] 
}

path "secret/data/password/*" {
  capabilities = ["create","update"]
}
