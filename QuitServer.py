import sys
import time
import socket
import Settings

def QuitServer():
    serverIpAddr = ['','']

    serverAddr0 = ("255.255.255.255", Settings.port0)
    s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s0.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s0.bind(('', Settings.port0))

    ############################################################################################
    # State 1. Let the Handshaking begin. Send initial request to server
    ############################################################################################
    maxInitAttempts = 50
    prefix = "S"
    for ii in range(1, maxInitAttempts, 1):
        quitmsg = 'QUIT'
        msg = 'DataClient:   State 1. %sending QUIT broadcast message (attempt #%d) to server to (%s, %d)\n'% \
              (prefix, ii, serverAddr0[0], serverAddr0[1])
        bannerStr = ('*' * len(msg)) + '\n'
        sys.stdout.write(bannerStr)
        sys.stdout.write(msg)
        sys.stdout.write(bannerStr)
        s0.sendto(msg.encode('utf-8'), serverAddr0)
        time.sleep(.5)
        sys.stdout.write('\n')

        ############################################################################################
        # State 2. Immediately start waiting to receive server IP address
        ############################################################################################
        message = ''
        maxRecvAttempts = 5
        for ii in range(1, maxRecvAttempts, 1):
            sys.stdout.write('DataClient:   State 2. Attempt #%d to receive response from server on port %d ...\n'% (ii, Settings.port1))
            try:
                message, serverIpAddr = s1.recvfrom(256)
                if len(message) > 0:
                    break
                sys.stdout.write('DataClient:   State 2. Timed out waiting for server response. Will try again ...\n')
                sys.stdout.write('\n')
            except socket.error:
                sys.stdout.write('DataClient:   State 2. Error generated while waiting for server response. Will try again ...\n')
                sys.stdout.write('\n')
                pass
        prefix = "Re-S"
        if len(message) > 0:
            break

    # Handle failure to connect to server by exiting
    if not message:
        sys.stdout.write('DataClient:   State 2. Did not receive response from server ... Exiting \n')

    sys.stdout.write('\n')
    return serverIpAddr, s1, message

