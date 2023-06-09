import sys
from DataServer import DataServer
from DataClient import DataClient
from QuitServer import QuitServer
from Logger import Logger
import Settings

logger = Logger('NinjaNIRS_ClientServer')

# --------------------------------------------------------------------
if __name__ == '__main__':
    while True:
        if len(sys.argv) < 2:
            sys.stdout.write('ERROR: no argument supplied\n')
            quit(1)
        logger.Write('WELCOME to NinjaNIRS_ClientServerTCP:  %s\n'% sys.argv[1])
        logger.CurrTime()
        Settings.Print()
        if sys.argv[1] == 'client':
            DataClient(logger)
            break
        elif sys.argv[1] == 'server':
            if DataServer(logger) == 0:
                break
        elif sys.argv[1] == 'quit':
            QuitServer(logger)
            break
    logger.Close()

