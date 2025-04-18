import mysql.connector, sys, time

from modules.strings import Console
from modules.config import Config
from modules.strings import Console
from modules.log import LOG
from modules.tools import network, TimeDo

accounts = {}
usernames = []
logs = []
perm = {}
permusers = []
permlist = []

class sql():
    def __init__(self):
        try:
            self.araax = mysql.connector.connect(host=network(), user=Config.read()['sql']['username'], password=Config.read()['sql']['password'], database=Config.read()['sql']['database'], auth_plugin='mysql_native_password')
            self.cursor = self.araax.cursor()
            if self.araax.is_connected():
                LOG.info(Console.ConnSQLSuccess.value.format(ip=network()))
            else:
                self.araax.reconnect()
        except:
            LOG.error(Console.ConnSQLError.value.format(ip=network()))
            sys.exit(1)
    
    def MakeOffline(self):
        self.araax.reconnect()
        self.cursor.execute(f"UPDATE users SET logedin = '0'")
        self.araax.commit()
        LOG.info(Console.OfflineUsers.value)
    
    def ReadAccounts(self):
        start = time.perf_counter()
        self.cursor.execute('SELECT * FROM users')
        for row in self.cursor:
            accounts[row[1]] = {'id': row[0], 'username': row[1], 'password': row[2], "logedin": row[3]}
        LOG.info(Console.Load.value.format(number=len(accounts), table="users", time=TimeDo(start)))
        return accounts
    
    def ReadUsernames(self):
        usernames = []
        self.cursor.execute('SELECT * FROM users')
        for row in self.cursor:
            usernames.append((row[1], row[1]))
        return usernames

    def Readpermusers(self):
        permusers = []
        self.cursor.execute('SELECT * FROM users')
        for row in self.cursor:
            permusers.append((row[0], row[1]))
        return permusers
    
    def SearchSQL(self):
        counter = 1
        IDList = []
        self.cursor.execute('SELECT * FROM users')
        datas = self.cursor.fetchall()
        for data in datas:
            IDList.append(data[0])
        while True:
            if counter not in IDList:
                return counter
            else:
                counter += 1

    def ReadPerm(self):
        start = time.perf_counter()
        self.cursor.execute('SELECT * FROM perm')
        for row in self.cursor:
            perm[row[0]] = {'delete': row[1], 'upload': row[2], 'newfolder': row[3], 'rename': row[4], 'log': row[5], 'admin': row[6], 'print': row[7], 'search': row[8]}
        LOG.info(Console.Load.value.format(number=len(accounts), table="perm", time=TimeDo(start)))
        return perm
    
    def AfterReadPerm(self):
        permlist = []
        try:
            if not self.araax.is_connected():
                LOG.warning(Console.SQLReconnect.value)
                self.araax.reconnect()
            self.cursor.execute('SELECT * FROM perm')
        except mysql.connector.Error as err:
            LOG.error(Console.ConnSQLError.value)
        for row in self.cursor:
            permlist.append({'id': row[0], 'delete': row[1], 'upload': row[2], 'newfolder': row[3], 'rename': row[4], 'log': row[5], 'admin': row[6], 'print': row[7], 'search': row[8]})
        return permlist
    
    def InsertPerm(self, id):
        self.araax.reconnect()
        self.cursor.execute("INSERT INTO perm (id, `delete`, upload, newfolder, `rename`, log, admin, `print`, search) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s)", (int(id), 0, 0, 0, 0, 0, 0, 0, 0))
        self.araax.commit()
        perm[id] = {'delete': 0, 'upload': 0, 'newfolder': 0, 'rename': 0, 'log': 0, 'admin': 0, 'print': 0, 'search': 0}
        permlist.append({'id': 0, 'delete': 0, 'upload': 0, 'newfolder': 0, 'rename': 0, 'log': 0, 'admin': 0, 'print': 0, 'search': 0})

    def Register(self, username, password):
        RegID = self.SearchSQL()
        self.araax.reconnect()
        self.cursor.execute("INSERT INTO users (id, username, password, logedin) VALUES (%s, %s, %s, %s)", (RegID, username, password, 0))
        self.araax.commit()
        accounts[username] = {'id': RegID, 'username': username, 'password': password, 'logedin': 0}
        usernames.append(username)
        self.InsertPerm(RegID)

    def Changepermission(self, userid, permissions):
        self.araax.reconnect()
        self.cursor.execute("""UPDATE perm SET `delete` = %s, upload = %s, newfolder = %s, `rename` = %s, log = %s, admin = %s, `print` = %s, search = %s WHERE id = %s""", (permissions['delete'], permissions['upload'], permissions['newfolder'], permissions['rename'], permissions['log'], permissions['admin'], permissions['print'], permissions['search'], userid ))
        self.araax.commit()
        perm[int(userid)].update(permissions)

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

    def UpdateUserOnline(self, username, online):
        self.araax.reconnect()
        self.cursor.execute(f"UPDATE users SET logedin = '{online}' WHERE username = '{username}'")
        self.araax.commit()

SQL = sql()