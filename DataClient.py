import sys
import time
import socket
import Settings

def RecvData():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #####################################################################
    # Dterming and send server it's IP address
    #####################################################################
    serverIpAddr, s1 = GetServerIpAddr()

    #####################################################################
    # Connect to server and receive data stream
    #####################################################################
    count = 0
    while count < 4:
        try:
            sys.stdout.write('DataClient:   5. Attempt #%d to connect to %s on port %d\n'% (count, serverIpAddr, Settings.port))
            err = s.connect_ex((serverIpAddr, Settings.port))
            if err == 0:
                break
            sys.stdout.write('DataClient:  Failed to connect on port %d\n\n'% Settings.port)
        except:
            sys.stdout.write('DataClient:  Failed to connect on port %d\n\n'% Settings.port)
        count = count+1
        time.sleep(1)
    if err != 0:
        sys.stdout.write('DataClient:   6. Exceeded max number of attempts to connect. Exiting ...\n')
        s1.sendto('Failed to connect, close connection'.encode('utf-8'), (serverIpAddr, Settings.port1))
        s.close()
        return

    sys.stdout.write('DataClient:   6. Connection Success!!\n')
    time.sleep(.5)

    # Receive data
    while True:
        d = s.recv(256)
        sys.stdout.write('Message from server received:  %s'% d.decode())
        if not d:
            break
    s.close()


# -------------------------------------------------------------------
def GetServerIpAddr():
    s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s0.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    serverAddr0 = ("255.255.255.255", Settings.port0)
    s0.bind(('', Settings.port0))
    s1.bind(('', Settings.port1))

    # 1. Let the Handshaking begin. Send initial request to server
    msg = 'DataClient:   1. Sending initial broadcat message to server\n'
    sys.stdout.write(msg)
    s0.sendto(msg.encode('utf-8'), serverAddr0)

    # 2. Immediatly start waiting to receive server IP address
    sys.stdout.write('DataClient:   2. Waiting to receive response from server\n')
    message, serverIpAddr = s1.recvfrom(256)

    # 3. Receive the client packet along with the address it is coming from
    sys.stdout.write('DataClient:   3. Received msg from server (IP: %s):  "%s"\n'% (serverIpAddr[0], message.decode()))
    time.sleep(2)

    # 4. Send server it's own IP address
    sys.stdout.write('DataClient:   4. Sending server its address %s ...\n'% serverIpAddr[0])
    serverAddr = (serverIpAddr[0], Settings.port1)
    s1.sendto(serverIpAddr[0].encode('utf-8'), serverAddr)

    return serverIpAddr


