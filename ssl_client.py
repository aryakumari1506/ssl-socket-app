# import socket
# import ssl

# def start_client():
#     """Start SSL client"""
#     # Client configuration
#     host = '127.0.0.1'
#     port = 8443
    
#     # Create a socket
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
#     # SSL context
#     context = ssl.create_default_context()
#     context.check_hostname = False
#     context.verify_mode = ssl.CERT_NONE  # In production, you should verify certificates
    
#     try:
#         # Connect to the server
#         client_socket.connect((host, port))
        
#         # Wrap the socket with SSL
#         ssl_socket = context.wrap_socket(client_socket, server_hostname=host)
        
#         print(f"Connected to {host}:{port}")
        
#         # Send data to server
#         message = "Hello, secure server!"
#         ssl_socket.sendall(message.encode())
        
#         # Receive response from server
#         data = ssl_socket.recv(1024)
#         print(f"Received: {data.decode()}")
        
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         ssl_socket.close()

# if __name__ == "__main__":
#     print("Starting SSL client...")
#     start_client()

import socket
import ssl

def start_client():
    """Start SSL client"""
    # Client configuration
    host = '127.0.0.1'
    port = 8443
    
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # In production, you should verify certificates
    
    try:
        # Connect to the server
        client_socket.connect((host, port))
        
        # Wrap the socket with SSL
        ssl_socket = context.wrap_socket(client_socket, server_hostname=host)
        
        print(f"Connected to {host}:{port}")
        
        # Send data to server
        message = "Hello, secure server!"
        ssl_socket.sendall(message.encode())
        
        # Receive response from server
        data = ssl_socket.recv(1024)
        print(f"Received: {data.decode()}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    print("Starting SSL client...")
    start_client()