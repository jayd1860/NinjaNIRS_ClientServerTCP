import sys
import time
import socket
import Settings


def SendData():
    # Set up a TCP/IP server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverIpAddr = socket.gethostbyname(Settings.servername)
    sys.stdout.write('DataServer:  Well-known server name is %s has IP address %s\n'% (Settings.servername, serverIpAddr))

    # Bind the socket to server (our own local) address and local port
    server_address = (serverIpAddr, Settings.port)
    sys.stdout.write('DataServer:  Binding socket to port %d\n'% Settings.port )
    tcp_socket.bind(server_address)

    # Listen on port 81
    tcp_socket.listen(1)

    while True:
        sys.stdout.write("DataServer:  Waiting for connection  ...\n")
        connection, client = tcp_socket.accept()
        time.sleep(2)
        count = 0

        try:
            sys.stdout.write("DataServer:  Connected to client IP: %s\n"% format(client))

            # Receive and print data 32 bytes at a time, as long as the client is sending something
            while True:
                connection.send('Message from SERVER'.encode('utf-8'))
                sys.stdout.write("DataServer:  Server sending data:    count = %d\n"% count)
                time.sleep(1)
                count = count+1


        finally:
            connection.close()