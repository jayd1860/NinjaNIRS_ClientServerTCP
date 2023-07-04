import numpy as np

port0 = 6037
port1 = 6038
port = 6021

N = 512
nRows = 256
wordSize = np.dtype(np.uint32).itemsize
chunkSize = N * wordSize
buff = np.uint32([range(0,N)] * nRows)
