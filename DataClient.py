import sys
import time
import socket
import Settings

def RecvData():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #####################################################################
    # Send server it's IP address
    #####################################################################
    serverIpAddr = GetServerIpAddr()

    #####################################################################
    # Connect to server and receive data stream
    #####################################################################
    count = 0
    while count < 4:
        try:
            sys.stdout.write('DataClient:  Attempt #%d to connect to socket on port %d\n'% (count, Settings.port))
            err = s.connect_ex((serverIpAddr, Settings.port))
            if err == 0:
                break
            sys.stdout.write('DataClient:  Failed to connect on port %d\n\n'% Settings.port)
        except:
            sys.stdout.write('DataClient:  Failed to connect on port %d\n\n'% Settings.port)
        count = count+1
        time.sleep(.3)
    if err != 0:
        sys.stdout.write('DataClient:  Exceeded max number of attempts to connect. Exiting ...\n')
        s.close()
        return
    sys.stdout.write('DataClient:  Connection Success!!\n')
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
    s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s0.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        serverIpAddr0 = socket.gethostbyname(Settings.servername)
    except:
        sys.stdout.write('DataClient:   Failed to find host %s\n' % Settings.servername)
        if Settings.servername[-1] == '\n':
            servernameTemp = Settings.servername[-1]
        else:
            servernameTemp = Settings.servername
        servernameAlt = (servernameTemp + '.local')
        sys.stdout.write('DataClient:   Will try host name %s\n' % servernameAlt)
        try:
            serverIpAddr0 = socket.gethostbyname(servernameAlt)
        except:
            serverIpAddr0 = '255.255.255.255'

    serverAddr = (serverIpAddr0, Settings.port0)
    s0.bind(('', Settings.port0))
    s0.sendto(serverIpAddr0.encode('utf-8'), serverAddr)
    time.sleep(1)

    # Receive the client packet along with the address it is coming from
    try:
        message, serverIpAddr = s0.recvfrom(128)
    except:
        sys.stdout.write(
            'DataClient:   recvfrom failed! Looks like server is offline. Waiting for server to come online ...\n')
        time.sleep(1)
        message, foo = s0.recvfrom(128)
    sys.stdout.write('DataClient:   Received confirmation from server (IP: %s)  - %s!!! ...\n'% (serverIpAddr, message.decode()))
    sys.stdout.write('\n')
    time.sleep(2)


