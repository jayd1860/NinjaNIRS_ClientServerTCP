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

    sys.stdout.write('\n')


    #####################################################################
    #  State 4:  Attempt to connect to server streamer
    #####################################################################
    err = -1
    for count in range(1, 5, 1):
        try:
            sys.stdout.write('DataClient:   State 4. Attempt #%d to connect to server data streamer at IP addr %s, port %d\n'%
                             (count, serverIpAddr, Settings.port))
            err = s.connect_ex((serverIpAddr, Settings.port))
            if err == 0:
                break
            sys.stdout.write('DataClient:  State 4. Failed to connect on port %d\n'% Settings.port)
        except:
            sys.stdout.write('DataClient:  State 4. Failed to connect on port %d\n'% Settings.port)
        time.sleep(1)
    if err != 0:
        sys.stdout.write('DataClient:   State 4. Exceeded max number of attempts to connect. Exiting ...\n')
        s1.sendto('Failed to connect, close connection'.encode('utf-8'), (serverIpAddr, Settings.port1))
        s.close()
        return
    sys.stdout.write('\n')


    #####################################################################
    #  State 5:  Connected to server stream.  Receive data
    #####################################################################
    sys.stdout.write('DataClient:   State 5. Connection Success!!\n')
    time.sleep(.5)
    while True:
        d = s.recv(256)
        if len(d)==0:
            break
        sys.stdout.write('DataClient:   State 5: Message from server received:  \"%s\"\n' % d.decode())
    s.close()
    sys.stdout.write('\n')



# -------------------------------------------------------------------
def GetServerIpAddr():
    s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s0.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.settimeout(1)

    serverIpAddr = ['','']
    serverAddr0 = ("255.255.255.255", Settings.port0)
    s0.bind(('', Settings.port0))
    s1.bind(('', Settings.port1))

    #### State 1. Let the Handshaking begin. Send initial request to server
    msg = 'DataClient:   State 1. Sending INITIAL broadcast message to server to port %d\n'% serverAddr0[1]
    sys.stdout.write(msg)
    s0.sendto(msg.encode('utf-8'), serverAddr0)

    #### State 2. Immediately start waiting to receive server IP address
    message = ''
    for ii in range(0, 10, 1):
        sys.stdout.write('DataClient:   State 2. Waiting maximum of 10 seconds to receive response from server ... attempt #%d\n'% ii)
        try:
            message, serverIpAddr = s1.recvfrom(256)
        except socket.error:
            sys.stdout.write('DataClient:   State 2. Timed out waiting for server response. Will try again ...\n')
            pass

    #### State 2:  Handle failure to connect to server by exiting
    if not message:
        sys.stdout.write('DataClient:   State 2. Was not able to connect to server ... Exiting \n')
        return

    sys.stdout.write('\n')

    #### State 2. Receive the client packet along with the address it is coming from
    sys.stdout.write('DataClient:   State 3. Received msg from server (IP: %s):  "%s"\n'%
                     (serverIpAddr[0], message.decode()))

    ####          Send server its own IP address
    sys.stdout.write('DataClient:   State 3. Sending server its address %s ...\n'% serverIpAddr[0])
    serverAddr = (serverIpAddr[0], Settings.port1)
    s1.sendto(serverIpAddr[0].encode('utf-8'), serverAddr)

    return serverIpAddr[0], s1


