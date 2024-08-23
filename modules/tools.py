import os, socket, time, sys, jdatetime
from datetime import datetime

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def GetDirServer():
    return os.path.split(os.path.abspath(__file__))

def network():
    return socket.gethostbyname(socket.gethostname())

def TimeDo(start):
    return round(time.perf_counter()-start, 2)

def Random():
    return str(os.urandom(12).hex)

def GetRootProject():
    return os.path.abspath(os.curdir)

def GetTime():
    return jdatetime.datetime.fromtimestamp(datetime.timestamp(datetime.now().replace(microsecond=0)))