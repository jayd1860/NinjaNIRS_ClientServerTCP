import sys
import GetTimeStamp
import numpy as np


# ----------------------------------------------------------
def ErrorReport(errs):
    sys.stdout.write('\n')
    if not errs:
        sys.stdout.write('No Errors\n')
        sys.stdout.write('\n')
        return

    if errs[0].find('Detected') < 0:
        _type = 'Generated'
    else:
        _type = 'Detected'

    banner = 'Errors %s:'% _type
    sys.stdout.write(banner+'\n')
    sys.stdout.write('%s'% '=' * len(banner))
    sys.stdout.write('\n')

    for ii in range(0,len(errs)):
        sys.stdout.write('%d. %s\n'% (ii+1, errs[ii]))
    sys.stdout.write('\n')



# ------------------------------------------------------------------
def GetDataRate(startTime, nWords):
    currTime = GetTimeStamp.datestr2datenum()
    return ((nWords*4) / (currTime - startTime)) / 1000.0

