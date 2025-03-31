#!/bin/bash
# Generate self-signed certificate for testing

# Generate private key
openssl genrsa -out server.key 2048

# Generate Certificate Signing Request (CSR)
openssl req -new -key server.key -out server.csr -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Generate self-signed certificate (valid for 365 days)
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

echo "SSL certificate generated. Files created:"
echo "- server.key (private key)"
echo "- server.csr (certificate signing request)"
echo "- server.crt (self-signed certificate)"