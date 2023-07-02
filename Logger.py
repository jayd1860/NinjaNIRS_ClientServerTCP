import os
import sys
import time

from GetAppDir import GetAppDir
from FileIO import GetFileSize


# -------------------------------------------------
def InitLogger(logger, name):
    if not not logger:
        return logger
    else:
        return Logger(name)


#############################################################
class OutputFlags(object):

    # -------------------------------------------------
    def __init__(self, options=None):
        self.NULL = -1
        self.CONSOLE_ONLY = 1
        self.FILE_ONLY = 2
        self.CONSOLE_AND_FILE = self.FILE_ONLY | self.CONSOLE_ONLY
        self.value = options


#############################################################
class Logger(object):

    # -------------------------------------------------
    def __init__(self, appname=None, options=None):

        if not appname:
            appname = 'History'

        self.appname = appname

        approotdir = GetAppDir()

        # Construct log file name
        self.filename = approotdir + '/' + appname + '.log'

        # Check if log file for this application already exists - if it does delete it so you can start fresh
        if os.path.exists(self.filename):
            if GetFileSize(self.filename) > 0:
                os.remove(self.filename)

        self.fhandle = open(self.filename, 'w')
        self.options = OutputFlags(options)



    # -------------------------------------------------
    def Write(self, s, options=None):
        # Value of internal options setting overrides options argument
        if self.options:
            options = self.options.value

        if options == self.options.NULL:
            return
        if not options:
            options = self.options.CONSOLE_AND_FILE
        if (options & self.options.FILE_ONLY) > 0:
            self.fhandle.write(s)
        if (options & self.options.CONSOLE_ONLY) > 0:
            sys.stdout.write(s)
            self.fhandle.flush()



    # -------------------------------------------------
    def CurrTime(self, options=None):
        ct = time.strftime("%a, %b %d %Y %H:%M:%S")
        s = '\n' + ct + '\n\n'
        if options == self.options.NULL:
            return
        if not options:
            options = self.options.CONSOLE_AND_FILE
        if (options & self.options.FILE_ONLY) > 0:
            self.fhandle.write(s)
        if (options & self.options.CONSOLE_ONLY) > 0:
            sys.stdout.write(s)
            self.fhandle.flush()
        return ct



    # -------------------------------------------------
    def Close(self):
        self.fhandle.close()
