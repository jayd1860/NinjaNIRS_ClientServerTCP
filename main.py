import sys

from DataServer import DataServer
from DataClient import DataClient
from QuitServer import QuitServer


if __name__ == '__main__':
    sys.stdout.write('WELCOME to ClientServer: arg1 == %s\n'% sys.argv[1])
    if sys.argv[1] == 'client':
        DataClient()
    elif sys.argv[1] == 'server':
        DataServer()
    elif sys.argv[1] == 'quit':
        QuitServer()

