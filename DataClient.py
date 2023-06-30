import sys
import time
import socket
import Settings

def RecvData():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #####################################################################
    #  State 2. Determine if we have server's IP address
    #####################################################################
    serverIpAddr, s1, message = GetServerIpAddr()
    if len(serverIpAddr)==0 or len(message)==0:
        s1.close()
        s.close()
        return
    sys.stdout.write('\n')


    ############################################################################################
    #  State 3:  Receive the client packet along with the address it is coming from.
    #            Attempt to connect to server streamer
    #####################################################################
    sys.stdout.write('DataClient:   State 3. Received msg from server (IP: %s):  "%s"\n'%
                     (serverIpAddr[0], message.decode()))

    # Send server its own IP address
    sys.stdout.write('DataClient:   State 3. Sending server its address %s to (%s, %d)...\n'% (serverIpAddr[0], serverIpAddr[0], Settings.port1))
    serverAddr = (serverIpAddr[0], Settings.port1)
    s1.sendto(serverIpAddr[0].encode('utf-8'), serverAddr)

    err = -1
    for count in range(1, 5, 1):
        try:
            sys.stdout.write('DataClient:   State 3. Attempt #%d to connect to server data streamer at (%s, %d)\n'%
                             (count, serverIpAddr[0], Settings.port))
            err = s.connect_ex((serverIpAddr[0], Settings.port))
            if err == 0:
                break
            sys.stdout.write('DataClient:  State 3. Failed to connect on port %d\n'% Settings.port)
        except:
            sys.stdout.write('DataClient:  State 3. Failed to connect on port %d\n'% Settings.port)
        time.sleep(1)
    if err != 0:
        sys.stdout.write('DataClient:   State 3. Exceeded max number of attempts to connect. Exiting ...\n')
        s1.sendto('Failed to connect, close connection'.encode('utf-8'), (serverIpAddr[0], Settings.port1))
        s.close()
        return
    sys.stdout.write('\n')


    #####################################################################
    #  State 5:  Connected to server stream.  Receive data
    #####################################################################
    sys.stdout.write('DataClient:   State 4. Connection Success!!\n')
    time.sleep(.5)
    while True:
        d = s.recv(256)
        if len(d)==0:
            break
        sys.stdout.write('DataClient:   State 4: Message from server received:  \"%s\"\n' % d.decode())
    s.close()
    sys.stdout.write('\n')



# -------------------------------------------------------------------
def GetServerIpAddr():
    serverIpAddr = ['','']

    serverAddr0 = ("255.255.255.255", Settings.port0)
    #serverAddr0 = ("192.168.87.60", Settings.port0)
    s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s0.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s0.bind(('', Settings.port0))

    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.settimeout(1)
    s1.bind(('', Settings.port1))


    ############################################################################################
    # State 1. Let the Handshaking begin. Send initial request to server
    ############################################################################################
    maxInitAttempts = 10
    prefix = "S"
    for ii in range(1, maxInitAttempts, 1):
        msg = 'DataClient:   State 1. %sending INITIAL broadcast message to server to (%s, %d)\n'% \
              (prefix, serverAddr0[0], serverAddr0[1])
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


