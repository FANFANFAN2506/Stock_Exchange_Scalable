import socket
from parse import *


def client_send(request):
    # create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # connect the socket to a specific address and port
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)
    print('Connected to', server_address)
    client_socket.sendall(request.encode())
    print("Request sent")
    # receive data from server
    response = client_socket.recv(1024)
    print('Received data:', response.decode())
    # close the connection
    client_socket.close()


def constructOrderString(id, args):
    print(args.key(), args.value())
    return f'<transactions id=\"{id}\"><order sym=\"X\" amount=\"300\" limit=\"125\"/></transactions>'


if __name__ == '__main__':
    # xmlString = "<create><account id=\"1\" balance=\"200000\"/><account id=\"2\" balance=\"200000\"/><account id=\"3\" balance=\"200000\"/><account id=\"4\" balance=\"200000\"/><account id=\"5\" balance=\"200000\"/><account id=\"6\" balance=\"2000000\"/><account id=\"7\" balance=\"200000\"/>"
    # xmlString += "<symbol sym=\"X\"><account id=\"1\">1000</account><account id=\"2\">1000</account><account id=\"3\">1000</account><account id=\"4\">1000</account><account id=\"5\">1000</account><account id=\"6\">1000</account><account id=\"7\">1000</account></symbol></create>"
    # client_send(xmlString)
    # # args = {0: 0, 300: 125, -100: 130, 200: 127, -
    # #         500: 128, -200: 140, 400: 125, -400: 124}
    # # for i in range(1, 7):
    # #     print(constructOrderString(i, args[i]))
    # xmlString1 = "<transactions id=\"1\"><order sym=\"X\" amount=\"300\" limit=\"125\"/></transactions>"
    # client_send(xmlString1)
    # xmlString2 = "<transactions id=\"2\"><order sym=\"X\" amount=\"-100\" limit=\"130\"/></transactions>"
    # client_send(xmlString2)
    # xmlString3 = "<transactions id=\"3\"><order sym=\"X\" amount=\"200\" limit=\"127\"/></transactions>"
    # client_send(xmlString3)
    # xmlString4 = "<transactions id=\"4\"><order sym=\"X\" amount=\"-500\" limit=\"128\"/></transactions>"
    # client_send(xmlString4)
    # xmlString5 = "<transactions id=\"5\"><order sym=\"X\" amount=\"-200\" limit=\"140\"/></transactions>"
    # client_send(xmlString5)
    # xmlString6 = "<transactions id=\"6\"><order sym=\"X\" amount=\"400\" limit=\"125\"/></transactions>"
    # client_send(xmlString6)
    # xmlString7 = "<transactions id=\"7\"><order sym=\"X\" amount=\"-400\" limit=\"124\"/></transactions>"
    # client_send(xmlString7)
    xmlString = "<create><account id=\"1\" balance=\"10000\"/><symbol sym=\"X\"><account id=\"1\">1000</account></symbol></create>"
    client_send(xmlString)
    # for i in range(1, 5):
    xmlString1 = "<transactions id=\"1\"><order sym=\"X\" amount=\"10\" limit=\"10\"/></transactions>"
    client_send(xmlString1)
    xmlString2 = "<transactions id=\"1\"><order sym=\"X\" amount=\"-10\" limit=\"10\"/></transactions>"
    client_send(xmlString2)
