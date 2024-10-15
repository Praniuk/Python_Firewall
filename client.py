import socket

def send_packets(target_ip, target_port, message):
    # Create a TCP client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the receiving device (firewall) by IP and port
    client_socket.connect((target_ip, target_port))
    
    # Send the message
    client_socket.sendall(message.encode('utf-8'))
    print(f"Sent message: {message}")
    
    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    target_ip = '192.168.0.44'  # Replace with the IP of the receiving device
    target_port = 8080           # The port the server is listening on
    message = "Hellooooo from client!"
    
    send_packets(target_ip, target_port, message)
