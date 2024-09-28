import socket

# TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("127.0.0.1", 8080))
server_socket.listen(5)  # Connections

# Received Data
data = server_socket.recv(1024)

print(f"Received Data: {data}")

server_socket.close()
