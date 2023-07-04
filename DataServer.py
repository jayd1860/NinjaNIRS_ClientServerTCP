import sys
import time
import socket
import numpy as np
import Settings
from Settings import buff


# ---------------------------------------------------------------------------
def DataServer(logger):
    streamSocketBound = False

    # Receive own IP address on this socket
    server_address1 = ('', Settings.port1)
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.settimeout(.5)
    s1.bind(server_address1)

    # Data stream socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(60)

    while True:         # This is main server loop for an entire aquisition session

        while True:         # This is the loop for getting our own IP address. If it fails we go back to state 1

            #####################################################################
            # State 1-2: Get your own IP address from client
            #####################################################################

            # Set up initial request socket
            server_address0 = ('', Settings.port0)
            s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            s0.bind(server_address0)

            #  State 1. Waiting to receive initial request from client
            msg = 'DataServer:   State 1. Waiting to receive INITIAL MESSAGE from client on port %d...\n'% Settings.port0
            bannerStr = ('*' * len(msg)) + '\n'
            logger.Write(bannerStr)
            logger.Write(msg)
            logger.Write(bannerStr)
            initClientMsg, clientIpAddr = s0.recvfrom(256)
            logger.Write('\n')
            time.sleep(.5)

            # Create stream socket
            serverIpAddr = ''
            maxRecvAttempts = 10
            for count in range(1, maxRecvAttempts):
                #  State 2. Received initial request. Send client confirmation of INITIAL message receipt
                msg = 'DataServer:   State 2. Received INITIAL MESSAGE from client (%s, %s). Sending response to (%s, %d)...'% \
                        (clientIpAddr[0], clientIpAddr[1], clientIpAddr[0], Settings.port1)
                logger.Write(msg + '\n')
                s1.sendto(msg.encode('utf-8'), (clientIpAddr[0], Settings.port1))
                time.sleep(.5)

                # State 2. Wait to receive our own IP address
                logger.Write('DataServer:   State 2. Waiting to receive our own IP address from client ... attempt #%d\n'% count)
                try:
                    serverIpAddr, clientIpAddr = s1.recvfrom(256)
                    if len(serverIpAddr) > 0:
                        break
                    logger.Write('DataServer:   State 2. Attempt #%d to receive own IP address timed out. Trying again ...\n'%  count)
                except socket.error:
                    logger.Write('DataServer:   State 2. Attempt #%d to receive own IP address generated ERROR. Trying again ...\n'%  count)
            sys.stdout.write('\n')
            if len(serverIpAddr) > 0:
                if serverIpAddr == 'Failed to connect, close connection':
                    continue
                break
            if initClientMsg.decode() == 'QUIT':
                logger.Write('Received QUIT command ... Exiting\n')
                return
            s0.close()
        sys.stdout.write('\n')


        ############################################################################################
        # State 3. We received our own IP address. Now move into new state - create and bind
        # stream socket to our IP address and port and then start listening on it for connection
        # request
        ############################################################################################
        server_address = (serverIpAddr.decode(), Settings.port)
        logger.Write('DataServer:   State 3. Received our own IP address %s from client\n'% serverIpAddr.decode())

        # Bind the socket to server (our own local) address and local port.
        # Bind stream socket only once for the life of a server session
        logger.Write('DataServer:   State 3. Opening, binding and listening on stream socket (%s, %d)\n'%
                         (serverIpAddr.decode(), Settings.port))
        if not streamSocketBound:
            s.bind(server_address)
            streamSocketBound = True

        # Listen for and accept client connection then stream data to it
        s.listen(1)
        logger.Write("DataServer:   State 3. Listening for connection  ...\n")
        try:
            s2, clientAddr = s.accept()
        except:
            logger.Write("DataServer:  State 3. Accept timed out ... Exiting\n\n")
            return
        time.sleep(2)
        logger.Write('\n')

        ############################################################################################
        # State 5.  Connection has been established. Move into new state - send data stream
        ############################################################################################
        logger.Write("DataServer:  State 4. Connected to client (%s, %d)\n"%  (clientAddr[0], clientAddr[1]))

        ThroughPutTest(s2, logger)

        # Wait before closing connection to let last packet be received
        time.sleep(2)
        s2.shutdown(1)
        s2.close()
        logger.Write(msg+'\n\n\n')
        s0.close()



# --------------------------------------------------------------------
def ThroughPutTest(s, logger):
    sz = buff.shape
    for iRow in range(0, sz[0]):
        chunk = buff[iRow].tobytes()
        chunk0 = np.frombuffer(chunk, np.uint32)
        msg = ('DataServer:  Sending  chunk #%d:   first word=%d ... last word=%d\n'% (iRow+1, chunk0[0], chunk0[sz[1]-1]))
        logger.Write(msg)
        s.send(chunk)
        time.sleep(.2)
