import sys
import time
import socket
import numpy as np
import Settings
import random
import rand
import Utils
import GetTimeStamp

nSimErrors = 0
s0 = socket.socket()
s1 = socket.socket()
s2 = socket.socket()
s = socket.socket()

# ---------------------------------------------------------------------------
def DataServer(logger):
    global s0
    global s1
    global s
    global s2

    streamSocketBound = False

    # Receive own IP address on this socket
    server_address1 = ('', Settings.port1)
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.settimeout(.5)
    s1.bind(server_address1)

    # Data stream socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(20)

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
                except Exception as err:
                    logger.Write('DataServer:   State 2. Attempt #%d to receive own IP address generated ERROR %s. Trying again ...\n'%  (count, err))
            sys.stdout.write('\n')
            if len(serverIpAddr) > 0:
                if serverIpAddr == 'DataClient:   Failed to connect, close connection':
                    Cleanup(logger)
                    return -1
                break
            if initClientMsg.decode() == 'QUIT':
                logger.Write('DataServer:   Received QUIT command ... Exiting\n')
                Cleanup(logger)
                return 0
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
        logger.Write("DataServer:   State 3. Listening for connection ...\n")
        try:
            s2, clientAddr = s.accept()
        except Exception as err:
            logger.Write("DataServer:  State 3. Accept ERROR %s ... Will attempt to restart server\n\n"% err)
            Cleanup(logger)
            return -1
        time.sleep(2)
        logger.Write('\n')


        ############################################################################################
        # State 5.  Connection has been established. Move into new state - send data stream
        ############################################################################################
        logger.Write("DataServer:  State 4. Connected to client (%s, %d)\n"%  (clientAddr[0], clientAddr[1]))

        startTime = GetTimeStamp.datestr2datenum()
        errsGenerated = ThroughPutTest(logger)
        endTime = GetTimeStamp.datestr2datenum()

        sys.stdout.write('Elapsed time:  %s (%s seconds) \n' % (GetTimeStamp.ElapsedTimeStr(endTime - startTime), endTime - startTime))

        # Wait before closing connection to let last packet be received
        time.sleep(2)
        if not errsGenerated:
            Cleanup(logger)
            logger.Write("DataServer:  State 4. Data transmission error ... Will attempt to restart server\n\n")
            return -1

        try:
            s2.shutdown(1)
            s2.close()
            logger.Write('\n\n')
            s0.close()
        except Exception as err:
            logger.Write('DataServer:  ERROR shuting down socket - %s\n\n'% err)

        Utils.ErrorReport(errsGenerated)



# --------------------------------------------------------------------
def ThroughPutTest(logger):
    global nSimErrors
    global s2

    s2.settimeout(8)
    buff = Settings.buff
    nSimErrors = 0
    errsGenerated = []
    msgCount = 1
    nErrors = 0
    maxNumErrors = 8
    for iChunk in range(0, Settings.nChunks):
        chunkID = iChunk % int(Settings.nChunksMax)
        buff = buff + np.uint32(Settings.N)
        chunkBytes = buff.tobytes()
        chunkWords = buff
        err, chunkBytes = SimErrors(chunkBytes)
        if err < 0:
            errmsg = '      DataServer:   ALERT! Generated simulated error in chunk #%d' % chunkID
            logger.Write(errmsg + '\n')
            errsGenerated.append(errmsg)

        # This is where we notify the user of what is happening and that we're still alive
        if (iChunk % Settings.displayInterval) == 0:
            msg2 = 'DataServer:  %d. Sending  chunk #%d   -  first word = %d ... last word = %d\n'% \
                   (msgCount, chunkID, chunkWords[0], chunkWords[-1])
            msgCount = msgCount+1
            logger.Write(msg2)

        try:
            s2.send(chunkBytes)
        except Exception as err:
            if nErrors > maxNumErrors:
                Cleanup(logger)
                return errsGenerated
            logger.Write('DataServer:  Transmission ERROR #%d - %s\n'% (nErrors, err))
            nErrors = nErrors+1
        time.sleep(Settings.transmissionDelay)

    return errsGenerated


# ----------------------------------------------------------
def SimErrors(chunkBytes):
    err = 0
    if not Settings.SIM_ERRORS:
        return err, chunkBytes
    r = rand.genRandomUint8Seq(1)
    if 116 < r[0] < 118:
        rIdx = random.randint(0,Settings.chunkSizeInBytes)
        rVal = random.randint(0,len(chunkBytes)-1)
        p = chunkBytes[rIdx]
        if p != rVal:
            chunkBytes2 = np.frombuffer(chunkBytes, np.uint8).copy()
            chunkBytes2[rIdx] = rVal
            err = -1
            chunkBytes = chunkBytes2.tobytes()
    return err, chunkBytes



# -----------------------------------------------------------
def Cleanup(logger):
    global s0
    global s1
    global s
    global s2

    try:
        s0.close()
    except:
        logger.Write('DataServer:   Cleanup ERROR s0 already closed\n')

    try:
        s1.close()
    except:
        logger.Write('DataServer:   Cleanup ERROR s1 already closed\n')

    try:
        s2.shutdown(1)
        s2.close()
    except:
        logger.Write('DataServer:   Cleanup ERROR s2 already closed\n')

    try:
        s.close()
    except:
        logger.Write('DataServer:   Cleanup ERROR s already closed\n')


