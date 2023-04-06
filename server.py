import socket
from parse import *
from dbTable import engine
from multiprocessing import Pool
import os
import traceback


def handle_client_xml(client_socket):
    # print(f"Run on {os.getpid()}, waiting for message")
    try:
        length = 0
        while(1):
            received_data = client_socket.recv(1).decode("utf-8")
            if received_data == "\n":
                break
            elif int(received_data) < 0 or int(received_data) > 9:
                raise ValueError(
                    "Inappropriate input for xml length")
            else:
                length = length * 10 + int(received_data)
        if length <= 0:
            raise ValueError(
                "Length cannot be 0")
        data = client_socket.recv(length)
        received_request = data.decode("utf-8")
        # print(f"Received xml {received_request}")
        response = parsing_XML(received_request)
        # send a response back to the client
        client_socket.sendall(response.encode("utf-8"))
        client_socket.close()
    except Exception as e:
        traceback.print_exc()
        client_socket.sendall(str(e))
        client_socket.close()


def initializer(l):
    """ensure the parent proc's database connections are not touched
    in the new connection pool"""
    engine.dispose(close=False)
    global lock
    lock = l


def serverLitsen():
    # create a TCP socket
    # pool = Pool(3)
    pool = Pool(3, initializer=initializer, initargs=(l,))
    # pool = Pool(2, initializer=initializer)
    init_Engine()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind the socket to a specific address and port
    server_address = ('localhost', 12345)
    print('Server is listening on {}:{}'.format(*server_address))
    server_socket.bind(server_address)
    server_socket.listen(100)
    socket_list = list()
    while(1):
        client_socket, addr = server_socket.accept()
        socket_list.append(client_socket)
        if len(socket_list) > 0:
            current_client = socket_list.pop(0)
            pool.apply_async(func=handle_client_xml, args=(current_client,))
