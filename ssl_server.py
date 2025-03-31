# import socket
# import ssl
# import threading

# def handle_client(conn, addr):
#     """Handle client connection"""
#     try:
#         print(f"Connected by {addr}")
        
#         # Receive data from client
#         data = conn.recv(1024)
#         if not data:
#             return
            
#         print(f"Received: {data.decode()}")
        
#         # Send response back to client
#         response = f"Server received: {data.decode()}"
#         conn.sendall(response.encode())
        
#     except Exception as e:
#         print(f"Error handling client: {e}")
#     finally:
#         conn.close()

# def start_server():
#     """Start SSL server"""
#     # Server configuration
#     host = '127.0.0.1'
#     port = 8443
    
#     # Create a socket
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
#     # Bind the socket to address and port
#     server_socket.bind((host, port))
    
#     # Listen for connections
#     server_socket.listen(5)
#     print(f"Server listening on {host}:{port}")
    
#     # SSL context
#     context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#     context.load_cert_chain(certfile='server.crt', keyfile='server.key')
    
#     try:
#         while True:
#             # Accept client connection
#             client_socket, addr = server_socket.accept()
            
#             # Wrap the socket with SSL
#             ssl_socket = context.wrap_socket(client_socket, server_side=True)
            
#             # Handle client in a new thread
#             client_thread = threading.Thread(target=handle_client, args=(ssl_socket, addr))
#             client_thread.daemon = True
#             client_thread.start()
            
#     except KeyboardInterrupt:
#         print("Server shutting down")
#     finally:
#         server_socket.close()

# if __name__ == "__main__":
#     print("Starting SSL server...")
#     start_server()


import socket
import ssl
import threading

def handle_client(conn, addr):
    try:
        print(f"Connected by {addr}")
        
        # Receive data from client
        data = conn.recv(1024)
        if not data:
            return
            
        print(f"Received: {data.decode()}")
        
        # Send response back to client
        response = f"Server received: {data.decode()}"
        conn.sendall(response.encode())
        
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        conn.close()

def start_server():
    host = '127.0.0.1'
    port = 8443
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    import datetime
    
    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Create a self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"State"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"City"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(key, hashes.SHA256())
    
    # Write key and cert to memory
    cert_bytes = cert.public_bytes(serialization.Encoding.PEM)
    key_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Save files
    with open('server.key', 'wb') as f:
        f.write(key_bytes)
    with open('server.crt', 'wb') as f:
        f.write(cert_bytes)
    
    print("Certificate and key files created.")
    
    # Load cert chain
    context.load_cert_chain('server.crt', 'server.key')
    
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to address and port
    server_socket.bind((host, port))
    
    # Listen for connections
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    
    try:
        with context.wrap_socket(server_socket, server_side=True) as ssl_socket:
            while True:
                # Accept client connection
                client_socket, addr = ssl_socket.accept()
                
                # Handle client in a new thread
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
                client_thread.daemon = True
                client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server_socket.close()

if __name__ == "__main__":
    print("Starting SSL server...")
    start_server()