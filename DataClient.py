import sys
import time
import socket
import Settings

def RecvData():
    s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverIpAddr = socket.gethostbyname(Settings.servername)
    s0.sendto('DataClient: Sending IP address to server', serverIpAddr)
    time.sleep(1)
    while True:
        # Receive the client packet along with the address it is coming from
        message, foo = s0.recvfrom(128)
        if len(message) > 0:
            break
        sys.stdout.write('DataClient:   Waiting to receive confirmation from server ...\n')
        time.sleep(1)

    sys.stdout.write('DataClient:   Received confirmation from server!!! ...\n')
    sys.stdout.write('\n')
    time.sleep(2)

    # Connect to server
    count = 0
    while count < 3:
        try:
            sys.stdout.write('DataClient:  Attempt #%d to connect to socket on port %d\n'% (count, Settings.port))
            err = s.connect_ex((serverIpAddr, Settings.port))
            if err == 0:
                break
            sys.stdout.write('DataClient:  Failed to connect on port %d\n\n' % Settings.port)
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
        d = s.recv(128)
        sys.stdout.write('DataClient:  Received message   %s\n'% d)
        if not d:
            break
    s.close()
