import sys
from DataServer import DataServer
from DataClient import DataClient
from QuitServer import QuitServer
from Logger import Logger

logger = Logger('NinjaNIRS_ClientServer')

# --------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stdout.write('ERROR: no argument supplied\n')
        quit(1)
    logger.Write('WELCOME to NinjaNIRS_ClientServerTCP:  %s\n'% sys.argv[1])
    logger.CurrTime()
    if sys.argv[1] == 'client':
        DataClient(logger)
    elif sys.argv[1] == 'server':
        DataServer(logger)
    elif sys.argv[1] == 'quit':
        QuitServer(logger)
    logger.Close()

