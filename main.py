import sys
import numpy as np
from DataServer import DataServer
from DataClient import DataClient
from QuitServer import QuitServer
from Logger import Logger
from Settings import buff, N, nRows

logger = Logger('DataServer')

# --------------------------------------------------------------------
def CreateBuffer():
    global buff
    global N
    global nRows
    buff = np.uint32([range(0,N)] * nRows)
    for iRow in range(0,nRows):
        buff[iRow] = buff[iRow] + (N * iRow)+1



# --------------------------------------------------------------------
if __name__ == '__main__':
    logger.Write('WELCOME to NinjaNIRS_ClientServerTCP:  %s\n'% sys.argv[1])
    logger.CurrTime()
    CreateBuffer()
    if sys.argv[1] == 'client':
        DataClient(logger)
    elif sys.argv[1] == 'server':
        DataServer(logger)
    elif sys.argv[1] == 'quit':
        QuitServer(logger)
    logger.Close()

