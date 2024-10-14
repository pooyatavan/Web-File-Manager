import mysql.connector, sys, time

from modules.strings import Console, Objects
from modules.config import Config
from modules.strings import Console
from modules.log import LOG
from modules.tools import network, TimeDo

accounts = {}
usernames = []
logs = []

class sql():
    def __init__(self):
        try:
            self.araax = mysql.connector.connect(host=network(),
                                                 database=Config.read()['sql']['database'],
                                                 user=Config.read()['sql']['username'],
                                                 password=Config.read()['sql']['password'],
                                                 port=int(Config.read()['sql']['port']))
            self.cursor = self.araax.cursor()
            if self.araax.is_connected():
                LOG.info(Console.ConnSQLSuccess.value.format(ip=Config.read()['sql']['ip']))
        except:
            LOG.error(Console.ConnSQLError.value.format(ip=Config.read()['sql']['ip']))
            sys.exit(1)
    
    def ReadAccounts(self):
        usernames.append((0, Objects.ChooseUsername.value))
        usernames.append((1, Objects.AllUsers.value))
        start = time.perf_counter()
        self.cursor.execute('SELECT * FROM users')
        for row in self.cursor:
            accounts[row[1]] = {'username': row[1], 'password': row[2], 'permission': row[3]}
            usernames.append((row[1], row[1]))
        LOG.info(Console.Load.value.format(number=len(accounts), table="users", time=TimeDo(start)))
        return accounts, usernames
    
    def Register(self, username, password, permission):
        self.araax.reconnect()
        self.cursor.execute("INSERT INTO users (username, password, permission) VALUES (%s, %s, %s)", (username, password, permission))
        self.araax.commit()
        accounts[username] = {'username': username, 'password': password, 'permission': permission}
        usernames.append(username)

    def Changepermission(self, username, permission):
        self.araax.reconnect()
        self.cursor.execute(f"UPDATE users SET permission = '{permission}' WHERE username = '{username}'")
        self.araax.commit()
        accounts[username].update({'permission': permission})

    def DeleteUsername(self, selectusername):
        self.araax.reconnect()
        self.cursor.execute(f"DELETE from users WHERE username = '{selectusername}'")
        self.araax.commit()
        accounts.pop(selectusername)

    def ChangePassword(self, username, password):
        self.araax.reconnect()
        self.cursor.execute(f"UPDATE users SET password = '{password}' WHERE username = '{username}'")
        self.araax.commit()
        accounts[username].update({'password': password})

    def ReadLogs(self, username):
        self.araax.reconnect()
        if username == "1":
            self.cursor.execute('SELECT * FROM logs')
        elif not username == "0" or "1":
            self.cursor.execute(f"SELECT * FROM logs WHERE user = '{username}'")
        logs = self.cursor.fetchall()
        return logs

    def InsertLog(self, number, date, username, operate, detail):
        self.araax.reconnect()
        self.cursor.execute("INSERT INTO logs (number, date, user, operate, detail) VALUES (%s, %s, %s, %s, %s)", (number, str(date), username, operate, detail))
        self.araax.commit()
        logs.append([number, date, username, operate, detail])

    def RemoveAllLogs(self):
        Delete_all_rows = """truncate table logs """
        self.cursor.execute(Delete_all_rows)
        self.araax.commit()
        return logs == []

SQL = sql()