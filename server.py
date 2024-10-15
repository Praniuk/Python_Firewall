import socket


def start_server(listen_ip, listen_port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the IP address and port
    server_socket.bind((listen_ip, listen_port))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Listening on {listen_ip}:{listen_port}...")
    
    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received data: {data}")
        
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    listen_ip = '0.0.0.0'  # Listen on all available interfaces
    listen_port = 8080      # Same port as the client is sending to
    
    start_server(listen_ip, listen_port)
