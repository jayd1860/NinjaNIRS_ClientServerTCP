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
    if len(serverIpAddr)==0:
        s1.close()
        s.close()
        return

    #####################################################################
    # Connect to server and receive data stream
    #####################################################################
    count = 1
    while count < 4:
        try:
            sys.stdout.write('DataClient:   5. Attempt #%d to connect to %s on port %d\n'%
                             (count, serverIpAddr, Settings.port))
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
        if len(d)==0:
            break
        sys.stdout.write('Message from server received:  \"%s\"\n' % d.decode())
    s.close()


# -------------------------------------------------------------------
def GetServerIpAddr():
    s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s0.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.settimeout(10)

    serverIpAddr = ['','']
    serverAddr0 = ("255.255.255.255", Settings.port0)
    s0.bind(('', Settings.port0))
    s1.bind(('', Settings.port1))

    # 1. Let the Handshaking begin. Send initial request to server
    msg = 'DataClient:   1. Sending initial broadcast message to server to port %d\n'% serverAddr0[1]
    sys.stdout.write(msg)
    s0.sendto(msg.encode('utf-8'), serverAddr0)

    # 2. Immediately start waiting to receive server IP address
    sys.stdout.write('DataClient:   2. Waiting maximum of 10 seconds to receive response from server\n')
    try:
        message, serverIpAddr = s1.recvfrom(256)
    except:
        sys.stdout.write('DataClient:   ERROR: timed out waiting for server response. Exiting ...\n')
        s0.close()
        return serverIpAddr[0], s1

    # 3. Receive the client packet along with the address it is coming from
    sys.stdout.write('DataClient:   3. Received msg from server (IP: %s):  "%s"\n'%
                     (serverIpAddr[0], message.decode()))
    time.sleep(2)

    # 4. Send server its own IP address
    sys.stdout.write('DataClient:   4. Sending server its address %s ...\n'% serverIpAddr[0])
    serverAddr = (serverIpAddr[0], Settings.port1)
    s1.sendto(serverIpAddr[0].encode('utf-8'), serverAddr)
    time.sleep(2)

    return serverIpAddr[0], s1


