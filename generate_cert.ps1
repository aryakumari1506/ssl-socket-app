# Check if OpenSSL is installed
$openssl = Get-Command openssl -ErrorAction SilentlyContinue

if ($null -eq $openssl) {
    Write-Host "OpenSSL is not installed or not in your PATH. Please install OpenSSL and try again."
    Write-Host "You can download it from https://slproweb.com/products/Win32OpenSSL.html"
    exit
}

# Generate private key
Write-Host "Generating private key..."
openssl genrsa -out server.key 2048

# Generate Certificate Signing Request (CSR)
Write-Host "Generating certificate signing request..."
openssl req -new -key server.key -out server.csr -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Generate self-signed certificate
Write-Host "Generating self-signed certificate..."
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

Write-Host "SSL certificate generated. Files created:"
Write-Host "- server.key (private key)"
Write-Host "- server.csr (certificate signing request)"
Write-Host "- server.crt (self-signed certificate)"