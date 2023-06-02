import sys

from DataServer import SendData
from DataClient import RecvData

if __name__ == '__main__':
    sys.stdout.write('WELCOME to ClientServer: arg1 == %s\n'% sys.argv[1])
    if sys.argv[1] == 'client':
        RecvData()
    else:
        SendData()

