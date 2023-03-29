#include <netdb.h>
#include <sys/socket.h>
#include <unistd.h>

#include <cstring>
#include <iostream>
#include <string>

#define PORT "12345"
#define MAXPENDING 10

using namespace std;

void serverListen() {
  int status;
  int socket_fd;
  struct addrinfo host_info;
  struct addrinfo *host_info_list, *a;
  const char * hostname = "0.0.0.0";
  const char * port = PORT;

  memset(&host_info, 0, sizeof(host_info));

  host_info.ai_family = AF_UNSPEC;
  host_info.ai_socktype = SOCK_STREAM;
  host_info.ai_flags = AI_PASSIVE;

  //get addr info
  status = getaddrinfo(hostname, port, &host_info, &host_info_list);
  if (status != 0) {
    cerr << "ERROR cannot get address info for host \n";
    return;
  }

  //bind socket
  for (a = host_info_list; a != NULL; a = a->ai_next) {
    socket_fd = socket(a->ai_family, a->ai_socktype, a->ai_protocol);
    if (socket_fd == -1) {
      cerr << "ERROR cannot create socket \n";
      continue;
    }
    int yes = 1;
    status = setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));
    status = bind(socket_fd, a->ai_addr, a->ai_addrlen);
    if (status == -1) {
      close(socket_fd);
      cerr << "ERROR cannot bind socket \n";
      continue;
    }
    break;
  }
  if (a == NULL) {
    cerr << "ERROR selectserver failed to bind \n";
    exit(EXIT_FAILURE);
  }

  // listen on socket
  freeaddrinfo(host_info_list);
  status = listen(socket_fd, MAXPENDING);
  if (status == -1) {
    cerr << "ERROR cannot listen on socket \n";
    return;
  }

  cout << "Waiting for connection on port " << port << endl;

  struct sockaddr_in socket_addr;
  socklen_t socket_addr_len = sizeof(socket_addr);
  int client_connection_fd;
  while (1) {
    client_connection_fd =
        accept(socket_fd, (struct sockaddr *)&socket_addr, &socket_addr_len);
    if (client_connection_fd == -1) {
      cerr << "Failed to establish connection with client" << endl;
    }
    else {
      //accept the connection, could read string.
    }
  }
}
