import os, socket, time, sys, jdatetime, re, eventlet, threading
from datetime import datetime

from modules.log import LOG
from modules.strings import Console

def thread(target):
    threading.Thread(target=target, daemon=True).start()
    
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def Silence():
    eventlet.sleep(604800)
    os._exit(0)

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

def CheckLetter(word):
    return bool(re.match(r'^[A-Za-z0-9.-]+$', word))

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

def ScanDir(BASE_DIR):
    start = time.perf_counter()
    folder_Search = []
    for root, dirs, files in os.walk(BASE_DIR):
        for dir in dirs:
            folder_Search.append(root.replace(BASE_DIR, "").replace("\\", "/") + "/" + dir)
    LOG.info(Console.DIRScan.value.format(count=len(folder_Search), time=TimeDo(start)))
    return folder_Search

def extract_sort_key(item):
    # Try to find a number inside parentheses
    match = re.search(r'\((\d+)\)', item)
    if match:
        return int(match.group(1))
    elif item.isdigit():
        return int(item)
    else:
        return float('inf')
    
def SortData(DataForSort):
    return sorted(DataForSort, key=lambda x: (extract_sort_key(x), x.lower()))
    # # numeric = sorted([w for w in DataForSort if w.isdigit()], key=int)
    # # non_numeric = sorted([w for w in DataForSort if not w.isdigit()])
    # test_entries = sorted(DataForSort, key=lambda x: int(x.split('(')[1].rstrip(')')))
    # FinalSorteFolder = test_entries
    # return FinalSorteFolder

def SlashRemover(Remover):
    return Remover.replace("\\", "/")