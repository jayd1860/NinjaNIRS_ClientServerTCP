import sys
import time
import socket
import Settings


def SendData():
    # Set up a TCP/IP server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to server (our own local) address and local port
    ipaddr = socket.gethostbyname(Settings.servername)
    server_address = (ipaddr, Settings.port)
    sys.stdout.write('DataServer:  Binding socket on IP address %s to port %d\n'% (ipaddr, Settings.port))
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