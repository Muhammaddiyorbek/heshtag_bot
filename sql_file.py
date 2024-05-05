import sqlite3 as sql

path='data.db'

class User:
    def __init__(self,dbName):
        self.tableName=dbName
        self.db=sql.Connection(path)
        self.cur=self.db.cursor()

    # def createTable(self):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.tableName} (user_id INT, full_name TEXT,my_referal TEXT,imkon INTEGER); """)
        self.db.commit()

    def getAllUsers(self):
        self.cur.execute(f""" SELECT * FROM {self.tableName} """)
        return self.cur.fetchall()

    def getAllUserId(self):
        self.cur.execute(f""" SELECT user_id FROM {self.tableName} """)
        return [user[0] for user in self.cur.fetchall()]

    def getSQL(self,user_id):
        self.cur.execute(f"""SELECT * FROM {self.tableName} WHERE user_id={user_id} """)
        return self.cur.fetchone()
    
    def getImkon(self, user_id):
        self.cur.execute(f"""SELECT imkon FROM {self.tableName} WHERE user_id={user_id} """)
        return self.cur.fetchone()[0]
    
    def configImkon(self,user_id,imkon_type):
        self.cur.execute(f"""UPDATE {self.tableName} SET imkon={imkon_type} WHERE user_id={user_id} """)
        self.db.commit()
    
    def addUser(self,user_id,full_name,my_referal,imkon=0):
        self.cur.execute(f"""INSERT INTO {self.tableName} (user_id,full_name,my_referal,imkon) VALUES  ({user_id},"{full_name}","{my_referal}",{imkon}); """)
        self.db.commit()


class Kanallar:
    def __init__(self,dbName):
        self.tableName=dbName
        self.db=sql.Connection(path)
        self.cur=self.db.cursor()

    # def createTable(self):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.tableName} (kanal_id INTEGER PRIMARY KEY AUTOINCREMENT, kanal_link TEXT UNIQUE); """)
        self.db.commit()
    
    def addSQL(self,kanal_link):
        try:
            self.cur.execute(f"""INSERT INTO {self.tableName} (kanal_link) VALUES  ("{kanal_link}"); """)
            self.db.commit()
            return True
        except:
            print("Bunday kanal_link mavjud")
            return False
    
    def getSQL(self):
        self.cur.execute(f"""SELECT * FROM {self.tableName} """)
        return self.cur.fetchall()
    
    def getKanalLink(self):
        self.cur.execute(f"""SELECT kanal_link FROM {self.tableName} """)
        return [kanal[-1] for kanal in self.cur.fetchall()]
    

    def deleteSQL(self,kanal_link):
        self.cur.execute(f"""DELETE FROM {self.tableName} WHERE kanal_link="{kanal_link}" """)   
        self.db.commit()
        print("kanal o'chirildi")

class Adminlar:
    def __init__(self,dbName):
        self.tableName=dbName
        self.db=sql.Connection(path)
        self.cur=self.db.cursor()

    # def createTable(self):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.tableName} (admin_id INTEGER, admin_link TEXT UNIQUE); """)
        if not self.cur.execute(f"SELECT * FROM {self.tableName} WHERE admin_id=5721982763 ").fetchone():
            self.cur.execute(f"""INSERT INTO  {self.tableName} (admin_id,admin_link) VALUES  (5721982763,"Developer_Flutter_Uz"); """)
        self.db.commit()
    
    def addSQL(self,admin_id,admin_link):
        try:
            self.cur.execute(f"""INSERT INTO {self.tableName} (admin_id,admin_link) VALUES  ({admin_id},"{admin_link}"); """)
            self.db.commit()
            return True
        except:
            print("Bunday admin mavjud")
            return False
    
    def getSQL(self):
        self.cur.execute(f"""SELECT * FROM {self.tableName} """)
        return self.cur.fetchall()
    
    def getAdminId(self):
        self.cur.execute(f"""SELECT * FROM {self.tableName} """)
        return [admin[0] for admin in self.cur.fetchall()]
    
    def getAdminLink(self):
        self.cur.execute(f"""SELECT * FROM {self.tableName} """)
        return [admin[-1] for admin in self.cur.fetchall()]
    

    def deleteSQL(self,admin_link):
        self.cur.execute(f"""DELETE FROM {self.tableName} WHERE admin_link="{admin_link}" """)   
        self.db.commit()
        print("admin o'chirildi")

class Heshteglar:
    def __init__(self,dbName):
        self.tableName=dbName
        self.db=sql.Connection(path)
        self.cur=self.db.cursor()

    # def createTable(self):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.tableName} (heshteg_id INTEGER PRIMARY KEY AUTOINCREMENT,heshteg TEXT); """)
        self.db.commit()
    
    def addSQL(self,heshteg):
        try:
            self.cur.execute(f"""INSERT INTO {self.tableName} (heshteg) VALUES  ("{heshteg}"); """)
            self.db.commit()
            return True
        except:
            print("Bunday heshteg mavjud")
            return False
    
    def getSQL(self):
        self.cur.execute(f"""SELECT * FROM {self.tableName} """)
        return self.cur.fetchall()
    
    def getHeshtegId(self,heshteg_id):
        self.cur.execute(f"""SELECT * FROM {self.tableName} WHERE heshteg_id={heshteg_id} """)
        return self.cur.fetchone()
    

    def deleteSQL(self,heshteg_id):
        self.cur.execute(f"""DELETE FROM {self.tableName} WHERE heshteg_id={heshteg_id} """)
        self.db.commit()
        print("heshteg o'chirildi")
        return True
    
    
