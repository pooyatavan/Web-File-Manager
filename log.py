import datetime
from pyfiglet import figlet_format

from modules.strings import Console

class log:
    def __init__(self):
        self.format = "%d/%m/%Y %H:%M:%S"
        self.date = datetime.datetime.now().strftime(self.format)

    def logfile(self, label, date, msg):
        print(label, date, msg)
        with open('log.txt', 'a') as file:
            file.writelines(f'{label} {date} {msg} \n')
            file.close()

    def info(self, msg):
        self.logfile("[INF]", self.date, msg)
        
    def warning(self, msg):
        self.logfile("[WAR]", self.date, msg)

    def error(self, msg):
        self.logfile("[ERR]", self.date, msg)

    def debug(self, msg):
        self.logfile("[DEB]", self.date, msg)

    def clearlogfile(self, username):
        with open('log.txt', 'w'):      
            pass
        LOG.info(Console.LogClrear.value.format(username=username))
    
    def logo(self):
        print(figlet_format("Araax", font="standard", width=300))

LOG = log()