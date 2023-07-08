import numpy as np


# -----------------------------------------------------
def numdigits(x, base=None):
    if not base:
        base=10

    if not isinteger(x):
        return -1

    x = abs(x)

    if x==0:
        return 1

    if base == 10:
        if int(np.ceil(np.log10(x)))==np.log10(x):
            return int(np.log10(x)+1)
        return int(np.ceil(np.log10(x)))

    if base == 2:
        if int(np.ceil(np.log(x)))==np.log(x):
            return int(np.log(x)+1)
        return int(np.ceil(np.log(x)))



# -----------------------------------------------------
def isinteger(x):
    b = False
    if type(x) == int:
        b = True
    if type(x) == np.int:
        b = True
    if type(x) == np.int8:
        b = True
    if type(x) == np.int16:
        b = True
    if type(x) == np.int32:
        b = True
    if type(x) == np.uint8:
        b = True
    if type(x) == np.uint16:
        b = True
    if type(x) == np.uint32:
        b = True
    return b


# -----------------------------------------------------
def isBitSet(x, bidx):
    return (x & (1<<bidx)) > 0


