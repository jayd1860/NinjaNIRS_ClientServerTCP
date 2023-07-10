import sys
import time
import socket
import numpy as np
import Settings
import random
import rand
import Logger
import GetTimeStamp
import Utils

chunkSize = Settings.chunkSize

def DataClient(logger):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(15)

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
    count = 0
    chunkWordCurr = 0
    chunkWords = np.uint32([])
    errsDetected = []
    startTime = GetTimeStamp.datestr2datenum()
    while True:
        chunkWordCurr = chunkWordCurr + len(chunkWords)
        try:
            chunkBytes = s.recv(chunkSize)
        except:
            sys.stdout.write('DataClient:   State 4: ERROR: Timed out waiting for data ...\n')
            break

        if len(chunkBytes)==0:
            sys.stdout.write('DataClient:   State 4: No more data was received ...\n')
            break

        chunkWords = np.frombuffer(chunkBytes, np.uint32)
        if ErrorCheck(chunkWords, chunkWordCurr) < 0:
            errmsg = '      DataClient:   Detected ERRORS in chunk #%d'% count
            sys.stdout.write(errmsg + '\n')
            errsDetected.append(errmsg)

        # Notify user that we're still receiving
        if (count % Settings.displayInterval) == 0:
            if (len(chunkBytes) % Settings.wordSize) == 0:
                msg2 = 'DataClient:  Received  chunk #%d  -  first word = %d ... last word = %d.\n' % \
                      (count, chunkWords[0], chunkWords[-1])
                sys.stdout.write(msg2)
            else:
                sys.stdout.write('DataClient:   State 4:   WARNING: Received %d bytes. Fgiure out what to do here\n' % (len(chunkBytes)))

        count = count+1

    Utils.ErrorReport(errsDetected)
    endTime = GetTimeStamp.datestr2datenum()
    sys.stdout.write('Elapsed time:  %s (%s seconds)\n'% (GetTimeStamp.ElapsedTimeStr(endTime - startTime), endTime-startTime))
    sys.stdout.write('\n')
    s.close()



# -------------------------------------------------------------------
def GetServerIpAddr():
    serverIpAddr = ['','']

    serverAddr0 = ("255.255.255.255", Settings.port0)
    s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s0.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s0.bind(('', Settings.port0))

    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.settimeout(.1)
    s1.bind(('', Settings.port1))

    message = ''

    ############################################################################################
    # State 1. Let the Handshaking begin. Send initial request to server
    ############################################################################################
    maxInitAttempts = 50
    prefix = "S"
    for ii in range(1, maxInitAttempts, 1):
        msg = 'DataClient:   State 1. %sending INITIAL broadcast message (attempt #%d) to server to (%s, %d)\n'% \
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
        maxRecvAttempts = 5
        for kk in range(1, maxRecvAttempts, 1):
            sys.stdout.write('DataClient:   State 2. Attempt #%d to receive response from server on port %d ...\n'% (kk, Settings.port1))
            try:
                message, serverIpAddr = s1.recvfrom(256)
                if len(message) > 0:
                    break
                sys.stdout.write('DataClient:   State 2. Timed out waiting for server response. Will try again ...\n')
                sys.stdout.write('\n')
            except socket.error:
                sys.stdout.write('DataClient:   State 2. Error generated while waiting for server response. Will try again ...\n')
                sys.stdout.write('\n')
                continue
        prefix = "Re-S"
        if len(message) > 0:
            break

    # Handle failure to connect to server by exiting
    if not message:
        sys.stdout.write('DataClient:   State 2. Did not receive response from server ... Exiting \n')

    sys.stdout.write('\n')
    return serverIpAddr, s1, message



# ---------------------------------------------------------------
def ErrorCheck(chunkWordsNew, chunkWordCurr):
    chunkWordsExpected = np.uint32(range(chunkWordCurr, chunkWordCurr+len(chunkWordsNew)))
    b = all(chunkWordsExpected == chunkWordsNew)
    if b:
        err = 0
    else:
        err = -1
    return err


####################################################################################

# --------------------------------------------------------------------
def ThroughPutTest_Simulation(logger):
    buff = Settings.buff
    chunkWordCurr = 0
    errsGenerated = []
    errsDetected = []
    chunkWords = np.uint32([])
    for iChunk in range(0, Settings.nChunks):
        chunkWordCurr = chunkWordCurr + len(chunkWords)
        chunkID = iChunk % int(Settings.nChunksMax)
        buff = buff + np.uint32(Settings.N)
        chunkBytes = buff.tobytes()
        chunkWords = buff
        err, chunkBytes = SimErrors(chunkBytes)
        if err < 0:
            errmsg = '      DataServer:   ALERT! Generated simulated error in chunk #%d'% chunkID
            sys.stdout.write(errmsg+'\n')
            errsGenerated.append(errmsg)

        if (iChunk % Settings.displayInterval) == 0:
            msg2 = 'DataServer:  Sending  chunk #%d:   first word = %d ... last word = %d\n'% \
                   (chunkID, chunkWords[0], chunkWords[-1])
            sys.stdout.write(msg2)

        # Instead of s.send(chunkBytes), we have error check
        chunkWords = np.frombuffer(chunkBytes, np.uint32)
        if ErrorCheck(chunkWords, chunkWordCurr) < 0:
            errmsg = '      DataClient:   Detected ERRORS in chunk #%d'% chunkID
            sys.stdout.write(errmsg + '\n')
            errsDetected.append(errmsg)
        time.sleep(Settings.transmissionDelay)

    return errsGenerated, errsDetected



# ----------------------------------------------------------
def SimErrors(chunkBytes):
    r = rand.genRandomUint8Seq(1)
    err = 0
    if 234 < r[0] < 237:
        rIdx = random.randint(0, Settings.chunkSizeInBytes-1)
        rVal = random.randint(0, len(chunkBytes)-1)
        p = chunkBytes[rIdx]
        if p != rVal:
            chunkBytes2 = np.frombuffer(chunkBytes, np.uint8).copy()
            chunkBytes2[rIdx] = rVal
            err = -1
            chunkBytes = chunkBytes2.tobytes()
    return err, chunkBytes



# --------------------------------------------------------------------
if __name__ == '__main__':
    logger = Logger.Logger('DataClient ThroughPutTest_Simulation:')

    startTime = GetTimeStamp.datestr2datenum()
    errsGenerated, errsDetected = ThroughPutTest_Simulation(logger)
    endTime = GetTimeStamp.datestr2datenum()

    sys.stdout.write('\n')

    Utils.ErrorReport(errsGenerated)
    Utils.ErrorReport(errsDetected)

    sys.stdout.write('Elapsed time:  %s (%s seconds) \n'% (GetTimeStamp.ElapsedTimeStr(endTime - startTime), endTime-startTime))
