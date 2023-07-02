import os
import platform

# -----------------------------------------------------------------------
def GetAppDir():

    if  platform.system() == 'Windows':
        approotdir = 'c:/users/public/NinjaNIRS_ClientServerTCP'
    else:
        homepath = os.path.expanduser('~')
        approotdir = homepath + '/NinjaNIRS_ClientServerTCP'

    if not os.path.exists(approotdir):
        os.mkdir(approotdir)

    return approotdir

