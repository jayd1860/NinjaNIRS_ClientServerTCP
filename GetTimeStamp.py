import sys
import time
from datetime import datetime
import numpy as np

# -------------------------------------------------
def GetTimeStamp(option=None):
    if not option:
        option = 1

    if option == 1:
        return time.strftime("%a, %b %d %Y %H:%M:%S") + '\n\n'

    elif option == 2:
        # datetime object containing current date and time.
        now = datetime.now()

        # dd/mm/YY H:M:S.
        return now.strftime("%d/%m/%Y %H:%M:%S")



# -------------------------------------------------
def ElapsedTimeStr(nsec):

    hours   = np.floor(nsec / 3600)
    minutes = np.floor((nsec - (3600*hours)) / 60)
    seconds = nsec - (3600*hours + 60*minutes)

    if hours==1:
        hlabel = 'hour'
    else:
        hlabel = 'hours'

    if minutes==1:
        mlabel = 'minute'
    else:
        mlabel = 'minutes'

    if seconds==1:
        slabel = 'second'
    else:
        slabel = 'seconds'

    hPrefix = ''
    mPrefix = ''
    sPrefix = ''
    if hours<10:
        hPrefix = '0'
    if minutes<10:
        mPrefix = '0'
    if seconds<10:
        sPrefix = '0'

    #    s = '%d %s, %d %s,  %d %s'% (hours, hlabel, minutes, mlabel, seconds, slabel)
    s = '%s%d:%s%d:%s%d'% (hPrefix, hours, mPrefix, minutes, sPrefix, seconds)
    return s

    

# -----------------------------------------------------
if __name__ == "__main__":
    etInSec = 12029
    et = ElapsedTimeStr(etInSec)
    sys.stdout.write('Elapsed Time for %d is %s\n'% (etInSec, et))

