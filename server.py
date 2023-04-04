import socket
from parse import *
from multiprocessing import Pool
import os


def handle_client_xml(client_socket):
    print(f"Run on {os.getpid()}, waiting for message")
    data = client_socket.recv(1024)
    received_request = data.decode()
    # print(f"Received xml {received_request}")
    Session = sessionmaker(bind=engine)
    session = Session()
    response = parsing_XML(session, received_request)
    session.close()
    # send a response back to the client
    client_socket.sendall(response.encode())
    client_socket.close()


def initializer():
    """ensure the parent proc's database connections are not touched
    in the new connection pool"""
    engine.dispose(close=False)


def serverLitsen():
    # create a TCP socket
    pool = Pool(4, initializer=initializer)
    init_Engine()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind the socket to a specific address and port
    server_address = ('localhost', 12345)
    print('Server is listening on {}:{}'.format(*server_address))
    server_socket.bind(server_address)
    server_socket.listen(20)
    while(1):
        client_socket, addr = server_socket.accept()
        print(f"connected to {addr}")
        pool.apply_async(func=handle_client_xml, args=(client_socket,))
