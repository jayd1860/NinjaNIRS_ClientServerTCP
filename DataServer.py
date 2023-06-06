import sys
import time
import socket
import Settings


def SendData():
    s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #####################################################################
    # Get your own IP address from client
    #####################################################################
    # server_address0 = ('192.168.154.249', Settings.port0)
    # s0.bind(server_address0)
    # sys.stdout.write('DataServer:  Waiting to receive IP from client ...\n')
    # while True:
    #     # Receive the client packet along with the address it is coming from
    #     serverIpAddr, clientIpAddr = s0.recvfrom(128)
    #     if len(serverIpAddr) > 0:
    #         sys.stdout.write('DataServer:  Received own IP address %s\n'% serverIpAddr.decode())
    #         time.sleep(2)
    #         s0.sendto(b'DataServer: We received our IP address', (clientIpAddr[0], Settings.port0))
    #         break
    #     sys.stdout.write('DataServer: Waiting to receive IP from client ...\n')
    #     time.sleep(1)

    serverIpAddr = Settings.serveripaddr.encode('utf-8')

    #####################################################################
    # Listen for and accept client connection then stream data to it
    #####################################################################
    server_address = (serverIpAddr, Settings.port)

    # Bind the socket to server (our own local) address and local port
    sys.stdout.write('DataServer:  Binding socket to server IP address %s on port %d\n'% (serverIpAddr.decode(), Settings.port))
    s.bind(server_address)
    s.listen(1)
    sys.stdout.write("DataServer:  Waiting for connection  ...\n")
    connection, client = s.accept()
    time.sleep(2)
    sys.stdout.write("DataServer:  Connected to client IP: %s\n"% format(client))

    # Send data stream
    count = 1
    while True:
        msg = ("\"DataServer:  This is data packet #%d\"\n" % count)
        connection.send(msg.encode('utf-8'))
        sys.stdout.write(msg)
        time.sleep(1)
        count = count+1

