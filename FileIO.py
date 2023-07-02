import os
import sys
import platform


# ---------------------------------------------------------------------------
def FileIO(name):
    pathnameFull = ''

    # Find absolute path of file name (if it exists) using the sys.path search paths
    filenamePathfull = ''
    for ii in range(0, len(sys.path)):
        drive, pathname = os.path.splitdrive(sys.path[ii])
        pathname, dirname = os.path.split(pathname)
        if name==dirname:
            pathname = sys.path[ii]
        else:
            pathname = sys.path[ii] + '/' + name
        pathnameFull = os.path.abspath(pathname)
        if os.path.exists(pathnameFull):
            sys.stdout.write('FileIO: found file %s\n'% filenamePathfull)
            break
    return pathnameFull



# ---------------------------------------------------------------------------
def GetFileSize(fileobject):
    if type(fileobject)==str:
        if os.path.exists(fileobject):
            fd = open(fileobject)
        else:
            return -1
    else:
        fd = fileobject

    # Since we're changing file position, save the initial one, then restore 
    # it before exiting 
    p0 = fd.tell()

    fd.seek(0,2) # move the cursor to the end of the file
    size = fd.tell()

    # Restore original file position
    fd.seek(p0)

    if type(fileobject)==str:
        fd.close()

    return size



# ---------------------------------------------------------------------------
def path2universal(p):
    if  platform.system() == 'Windows':
        return p.replace('\\','/')


# ---------------------------------------------------------------------------
def mkdirfull(p):
    if type(p) != str:
        return -1

    if os.path.exists(p):
        return 0

    #os.mkdir(p) 

    proot, plast = os.path.split(p)
    mkdirfull(proot)
    os.mkdir(p)


# -----------------------------------------------------
def pathscompare(path1, path2):

    # If path type is not equal then return false
    if os.path.isfile(path1) != os.path.isfile(path2):
        return False

    if not os.path.exists(path1):
        return False

    if not os.path.exists(path2):
        return False

    # If paths are files, compare just the file names, then the folders
    if os.path.isfile(path1):
        p1,f1 = os.path.split(path1)
        p2,f2 = os.path.split(path2)
        if f1 != f2:
            return False
        path1 = p1
        path2 = p2

    fullpath1 = path1
    fullpath2 = path2

    # Compare folders
    currdir = path2universal(os.getcwd())

    if os.path.exists(path1):
        os.chdir(path1)
        fullpath1 = path2universal(os.getcwd())
    else:
        os.chdir(currdir)
        return False

    if os.path.exists(path2):
        os.chdir(path2)
        fullpath2 = path2universal(os.getcwd())
    else:
        os.chdir(currdir)
        return False

    os.chdir(currdir)

    if  platform.system() == 'Windows':
        return fullpath1.lower() == fullpath2.lower()
    else:
        return fullpath1 == fullpath2



