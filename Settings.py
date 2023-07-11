import sys
import numpy as np
import GetTimeStamp

port0   = 6037
port1   = 6038
port    = 6021

DEBUG = False
SIM_ERRORS = False

# All time units are in seconds
if DEBUG:
    chunkSizeInWords = 64
else:
    chunkSizeInWords = 256
N = chunkSizeInWords
wordSize = np.dtype(np.uint32).itemsize
chunkSizeInBytes = N * wordSize
chunkSize = chunkSizeInBytes
buff = np.uint32(range(0,N)) - N

# Desired data rate in chunks / second
if DEBUG:
    desiredDataRateInBytes = 10 * chunkSizeInBytes
else:
    desiredDataRateInBytes = pow(2,19)

desiredDataRateInChunks = int(desiredDataRateInBytes / chunkSizeInBytes)
processingTimePerChunk = .5
processingTimePerChunkInChunks = processingTimePerChunk * desiredDataRateInChunks
transmissionDelay = 1 / (desiredDataRateInChunks + processingTimePerChunkInChunks)
transmissionTimePerChunk = transmissionDelay

# Transmit for about 2 minutes
if DEBUG:
    nChunks = 64 * np.uint32(desiredDataRateInChunks)
else:
    nChunks = 120 * desiredDataRateInChunks

nChunksMax = 1e8

transmissionTimeTotal = transmissionTimePerChunk * nChunks

# How long to wait in units of chunks before displaying that you sent/received a chunk
if DEBUG:
    displayInterval = 10
else:
    displayInterval = 3 * desiredDataRateInChunks


# --------------------------------------------------------
def Print():
    sys.stdout.write('\n')
    sys.stdout.write('=============================================================\n')
    sys.stdout.write('Configuration Settings:\n')
    sys.stdout.write('-----------------------\n')
    sys.stdout.write('    chunkSizeInWords            = %d words\n'% N)
    sys.stdout.write('    N                           = %d words\n'% N)
    sys.stdout.write('    chunkSizeInBytes            = %d bytes\n'% chunkSizeInBytes)
    sys.stdout.write('    nChunks                     = %d\n'% nChunks)
    sys.stdout.write('    nChunksMax                  = %d\n'% nChunksMax)
    sys.stdout.write('    desiredDataRateInBytes      = %0.1f bytes\n'% desiredDataRateInBytes)
    sys.stdout.write('    desiredDataRateInChunks     = %d chunks\n'% desiredDataRateInChunks)
    sys.stdout.write('    processingTimePerChunk      = %0.4f sec\n'% processingTimePerChunk)
    sys.stdout.write('    transmissionDelay           = %0.4f sec\n'% transmissionDelay)
    sys.stdout.write('    transmissionTimePerChunk    = %0.4f sec\n'% transmissionTimePerChunk)
    sys.stdout.write('    transmissionTimeTotal       = %0.1f sec  (%s)\n'%
                     (transmissionTimeTotal, GetTimeStamp.ElapsedTimeStr(transmissionTimeTotal)))
    sys.stdout.write('    displayInterval             = %d chunks\n'% displayInterval)
    sys.stdout.write('=============================================================\n')
    sys.stdout.write('\n')



# --------------------------------------------------------------------
if __name__ == '__main__':
    Print()
