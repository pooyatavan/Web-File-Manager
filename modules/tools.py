import os, socket, time, sys, jdatetime, re
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

def RemoveIP():
    return "http://" + socket.gethostbyname(socket.gethostname()) + "/"

def RandomKey():
    return str(os.urandom(12).hex)

def CheckLetter(username):
    return bool(re.match(r'^[A-Za-z]+$', username))

def extract_number(filename):
    match = re.search(r'\((\d+)\)', filename)
    return int(match.group(1)) if match else float('inf')

def CheckDateFormat(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        return False
    
def FLBD(logs, start_date, end_date):
    dates = []
    for log in logs:
        if start_date <= log[1].split()[0].replace("-", "") <= end_date:
            dates.append(log)
    return dates