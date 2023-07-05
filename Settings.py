import sys
import numpy as np
# import math
import GetTimeStamp

port0   = 6037
port1   = 6038
port    = 6021

chunkSizeInWords = 256
nChunks = 2e6
nChunksMax = 1e8
N = chunkSizeInWords
wordSize = np.dtype(np.uint32).itemsize
chunkSizeInBytes = N * wordSize
chunkSize = chunkSizeInBytes
buff = np.uint32([range(0,N)])

# Desired data rate in chunks / second
desiredDataRateInBytes  = pow(2,19)
desiredDataRateInChunks = np.uint32(desiredDataRateInBytes / chunkSizeInBytes)
transmissionDelay = 1/desiredDataRateInChunks
transmissionTimePerChunk = transmissionDelay
transmissionTimeTotal = transmissionTimePerChunk * nChunks
displayInterval = 32
endBreakPoint = 1



# --------------------------------------------------------------------
if __name__ == '__main__':
    sys.stdout.write('\nSETTINGS:\n')
    sys.stdout.write('      N                           = %d\n'% N)
    sys.stdout.write('      chunkSizeInBytes            = %d\n'% chunkSizeInBytes)
    sys.stdout.write('      nChunks                     = %d\n'% nChunks)
    sys.stdout.write('      nChunksMax                  = %d\n'% nChunksMax)
    sys.stdout.write('      desiredDataRateInBytes      = %0.1f\n'% desiredDataRateInBytes)
    sys.stdout.write('      desiredDataRateInChunks     = %0.1f\n'% desiredDataRateInChunks)
    sys.stdout.write('      transmissionTimePerChunk    = %0.4f\n'% transmissionDelay)
    sys.stdout.write('      transmissionTimeTotal       = %0.1f seconds  (%s)\n'%
                     (transmissionTimeTotal, GetTimeStamp.ElapsedTimeStr(transmissionTimeTotal)))
    sys.stdout.write('      displayInterval             = %d\n\n'% displayInterval)

