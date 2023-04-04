import socket
from parse import *

# create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# connect the socket to a specific address and port
server_address = ('localhost', 12345)
client_socket.connect(server_address)
print('Connected to', server_address)
<<<<<<< HEAD
request = "142\n<create><account id=\"1\" balance=\"50000\"/><account id=\"2\" balance=\"100000\"/><symbol sym=\"TESLA\"><account id=\"1\">200</account></symbol></create>"
=======
request = "<create><account id=\"1\" balance=\"50000\"/><account id=\"2\" balance=\"100000\"/><symbol sym=\"X\"><account id=\"1\">200</account><account id=\"2\">200</account></symbol><symbol sym=\"TESLA\"><account id=\"1\">200</account><account id=\"2\">200</account></symbol></create>"
>>>>>>> 6b5bede15771adea22de7095a2427dfc08a8a7c5
client_socket.sendall(request.encode())
print("Request sent")
# receive data from server
response = client_socket.recv(1024)
print('Received data:', response.decode())
# close the connection
client_socket.close()
