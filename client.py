import socket
from parse import *

# create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# connect the socket to a specific address and port
server_address = ('localhost', 12345)
client_socket.connect(server_address)
print('Connected to', server_address)

# # send data to the server
# send_request = 'Hello from client'
# xmlString = "<create><account id=\"1\" balance=\"100000\"/><account id=\"2\" balance=\"100000\"/><account id=\"3\" balance=\"100000\"/><account id=\"4\" balance=\"100000\"/><account id=\"5\" balance=\"100000\"/><account id=\"6\" balance=\"100000\"/><account id=\"7\" balance=\"100000\"/>"
# xmlString += "<symbol sym=\"X\"><account id=\"1\">500</account><account id=\"2\">500</account><account id=\"3\">500</account><account id=\"4\">500</account><account id=\"5\">500</account><account id=\"6\">500</account><account id=\"7\">500</account></symbol></create>"
# xmlString1 = "<transactions id=\"1\"><order sym=\"X\" amount=\"300\" limit=\"125\"/></transactions>"
# xmlString2 = "<transactions id=\"2\"><order sym=\"X\" amount=\"-100\" limit=\"130\"/></transactions>"
# xmlString3 = "<transactions id=\"3\"><order sym=\"X\" amount=\"200\" limit=\"127\"/></transactions>"
# xmlString4 = "<transactions id=\"4\"><order sym=\"X\" amount=\"-500\" limit=\"128\"/></transactions>"
# xmlString5 = "<transactions id=\"5\"><order sym=\"X\" amount=\"-200\" limit=\"140\"/></transactions>"
# xmlString6 = "<transactions id=\"6\"><order sym=\"X\" amount=\"400\" limit=\"125\"/></transactions>"
# xmlString7 = "<transactions id=\"7\"><order sym=\"X\" amount=\"-400\" limit=\"124\"/></transactions>"

# client_socket.sendall(xmlString.encode())
# # receive data from server
# # response = client_socket.recv(1024)
# # print('Received data:', response.decode())

# client_socket.sendall(xmlString1.encode())
# # receive data from server
# # response = client_socket.recv(1024)
# # print('Received data:', response.decode())

# client_socket.sendall(xmlString2.encode())
# # receive data from server
# # response = client_socket.recv(1024)
# # print('Received data:', response.decode())

# client_socket.sendall(xmlString3.encode())
# # receive data from server
# # response = client_socket.recv(1024)
# # print('Received data:', response.decode())

# client_socket.sendall(xmlString4.encode())
# # receive data from server
# # response = client_socket.recv(1024)
# # print('Received data:', response.decode())

# client_socket.sendall(xmlString5.encode())
# # receive data from server
# # response = client_socket.recv(1024)
# # print('Received data:', response.decode())

# client_socket.sendall(xmlString6.encode())
# # receive data from server
# # response = client_socket.recv(1024)
# # print('Received data:', response.decode())

# client_socket.sendall(xmlString7.encode())
# # receive data from server
# # response = client_socket.recv(1024)
# # print('Received data:', response.decode())


request = "<create><account id=\"1\" balance=\"50000\"/><account id=\"2\" balance=\"100000\"/><symbol sym=\"TESLA\"><account id=\"1\">200</account></symbol></create>"
client_socket.sendall(request.encode())
print("Request sent")
# receive data from server
response = client_socket.recv(1024)
print('Received data:', response.decode())
# close the connection
client_socket.close()
