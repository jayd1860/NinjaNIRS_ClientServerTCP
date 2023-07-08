import sys
import time
import random
import numpy as np
import math
import mathlib
import GetTimeStamp

# -----------------------------------------------------
def rand(waittime=None):
    if not waittime:
        waittime = random.randint(30,100)
    time.sleep(waittime/1000)
    x = int(100000*time.time())
    r = x - int(x / 10000) * 10000
    return r


# -----------------------------------------------------
def genRandomUint8Seq(sz = None):
    sd = seedWithCurrTime()

    if not sz:
        sz = 2**16

    # Make sure size is divisible by 4
    sz = sz + 4 - (sz % 4)

    s = np.uint8([0]*sz)
    for ii in range(0, len(s)):
        s[ii] = random.randint(0,0xff)
    return s


# ---------------------------------------------------------------
def seedWithCurrTime():
    sd = GetTimeStamp.datestr2datenum()
    random.seed(sd % math.pow(2,31))
    return sd



# --------------------------------------------------------------------
if __name__ == '__main__':
    r0 = genRandomUint8Seq(1).tobytes()
    r1 = np.squeeze(r0[0:2]).tobytes()
    sys.stdout.write('Generated 16-bit rns = %d\n'% np.frombuffer(r1, np.uint16))
    sys.stdout.write('Generated 32-bit rns = %d\n'% np.frombuffer(r0, np.uint32))

