import socket

# create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# connect the socket to a specific address and port
server_address = ('localhost', 12345)
client_socket.connect(server_address)
print('Connected to', server_address)

# send data to the server
send_request = 'Hello from client'
client_socket.sendall(send_request.encode())

#receive data from server
response = client_socket.recv(1024);
print('Received data:', response.decode())

# close the connection
client_socket.close()
