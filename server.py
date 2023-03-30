import socket

# create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to a specific address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

while(1):
    # listen for incoming connections
    server_socket.listen(1)
    print('Server is listening on {}:{}'.format(*server_address))

    # accept a connection
    client_socket, client_address = server_socket.accept()
    print('Connected by', client_address)

    # receive data from the client
    data = client_socket.recv(1024)
    print('Received data:', data.decode())

    # send a response back to the client
    response = 'Hello from the server'
    client_socket.sendall(response.encode())

# close the connection
client_socket.close()
server_socket.close()
