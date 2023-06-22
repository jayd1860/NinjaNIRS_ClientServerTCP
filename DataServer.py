import sys
import time
import socket
import Settings


def SendData():
    streamSocketBound = False

    server_address0 = ('', Settings.port0)
    server_address1 = ('', Settings.port1)

    s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s0.bind(server_address0)
    s1.bind(server_address1)

    while True:

        #####################################################################
        # Get your own IP address from client
        #####################################################################
        # 1. Waiting to receive initial request from client
        sys.stdout.write('DataServer:   1. Waiting to receive INITIAL MESSAGE from client ...\n')
        initClientMsg, clientIpAddr = s0.recvfrom(256)

        # 2. Received initial request. Wait 2 seconds for client to get ready to receive,
        #    then send client it's own IP address
        time.sleep(2)
        msg = 'DataServer:   2. Received INITIAL MESSAGE from client. Sending response\n'
        sys.stdout.write(msg)
        s1.sendto(msg.encode('utf-8'), (clientIpAddr[0], Settings.port1))

        # 3. Wait to receive our own IP address
        sys.stdout.write('DataServer:   3. Waiting to receive our own IP addrees from client ...\n')
        time.sleep(2)
        serverIpAddr, clientIpAddr = s1.recvfrom(256)

        # 4. Wait to receive our own IP address
        sys.stdout.write('DataServer:   4. Receive our own IP addrees %s from client\n'% serverIpAddr.decode())


        #####################################################################
        # Listen for and accept client connection then stream data to it
        #####################################################################
        server_address = (serverIpAddr.decode(), Settings.port)
        sys.stdout.write('\n')

        # Bind the socket to server (our own local) address and local port
        sys.stdout.write('DataServer:   5. Opening and binding stream socket to IP address %s, port %d\n'% (serverIpAddr.decode(), Settings.port))

        # Bind stream socket only once for the life of a server session
        if not streamSocketBound:
            s.bind(server_address)
            streamSocketBound = True

        s.listen(1)
        sys.stdout.write("DataServer:   6. Waiting for connection  ...\n")
        connection, client = s.accept()
        time.sleep(2)
        sys.stdout.write("DataServer:  7. Connected to client IP: %s\n"% format(client))

        # Send data stream
        count = 1
        while count < 10:
            msg = ("\"DataServer:  This is data packet #%d\"\n" % count)
            connection.send(msg.encode('utf-8'))
            sys.stdout.write(msg)
            time.sleep(1)
            count = count+1

        # Wait before closing connection to let last packet be received
        msg = 'DataServer:  Sent last message and closed connection ... goodbye\n'
        connection.send(msg.encode('utf-8'))
        time.sleep(2)
        connection.close()
        sys.stdout.write(msg)

    s.close()
    s1.close()
    s0.close()


