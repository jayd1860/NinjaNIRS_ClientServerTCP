import sys
import time
from datetime import datetime
import numpy as np

standardFmt = '%Y, %b %d - %H:%M:%S'

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
def datestr2datenum(datetimeStr=None, fmt='%Y, %b %d - %H:%M:%S', startYear=2010):
    if not datetimeStr:
        datetimeStandardFmt = time.strftime(standardFmt)
    else:
        datetimeStandardFmt = datetime.datetime.strptime(datetimeStr, fmt).strftime(standardFmt)

    datetimeNum = 0

    START_YEAR     = startYear
    MONTHS         = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    NUMDAYSINMONTH = np.uint8([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

    base_yr  = 32140800   # 12*31*24*60*60
    base_mo  = 2678400    # 31*24*60*60;
    base_day = 86400      # 24*60*60;
    base_hr  = 3600       # 60*60;
    base_min = 60

    # '2023, July 07 - 08:59:53'
    year    = int(datetimeStandardFmt[0:4]) - START_YEAR
    month   = MONTHS.index(datetimeStandardFmt[6:9].lower())+1
    day     = int(datetimeStandardFmt[10:12])
    hour    = int(datetimeStandardFmt[15:17])
    minute  = int(datetimeStandardFmt[18:20])
    second  = int(datetimeStandardFmt[21:23])

    # Now that we have a numeric date, check it for errors
    if year<0:
        return
    if not month or month<1 or month>12:
        return
    if day<1 or day>NUMDAYSINMONTH[month]:
        return
    if hour<0 or hour>23:
        return
    if minute<0 or minute>59:
        return
    if second<0 or second>59:
        return

    datetimeNum = np.uint32(year*base_yr + month*base_mo + day*base_day + hour*base_hr + minute*base_min + second)
    return datetimeNum


# --------------------------------------------------------------------
if __name__ == '__main__':
    # dts0 = '2018, Jul 15 - 08:23:12'
    standardFmt = '%Y, %b %d - %H:%M:%S'
    dts0 = time.strftime(standardFmt)
    dtn = datestr2datenum(dts0)
    sys.stdout.write('Time  \"%s\"  in seconds since  \"2000, Jan 1 - 00:00:00\"  = %d\n'% (dts0, dtn))

    etInSec = 12029
    et = ElapsedTimeStr(etInSec)
    sys.stdout.write('Elapsed Time for %d is %s\n'% (etInSec, et))

