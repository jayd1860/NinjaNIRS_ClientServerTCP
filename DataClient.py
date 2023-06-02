import sys
import time
import socket
import Settings

def RecvData():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sys.stdout.write('\n')

    # Connect to server
    count = 0
    while count < 3:
        try:
            sys.stdout.write('DataClient:  Attempt #%d to connect to socket on port %d\n'% (count, Settings.port))
            err = s.connect_ex((Settings.host, Settings.port))
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
