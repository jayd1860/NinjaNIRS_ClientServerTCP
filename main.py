import sys

from DataServer import DataServer
from DataClient import DataClient
from QuitServer import QuitServer
from Logger import Logger

logger = Logger('DataServer')

if __name__ == '__main__':
    logger.Write('WELCOME to NinjaNIRS_ClientServerTCP:  %s\n'% sys.argv[1])
    logger.CurrTime()
    if sys.argv[1] == 'client':
        DataClient(logger)
    elif sys.argv[1] == 'server':
        DataServer(logger)
    elif sys.argv[1] == 'quit':
        QuitServer(logger)
    logger.Close()

