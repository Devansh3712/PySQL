'''
module for user and data
authentication
'''

import mysql.connector as mc

#class for maintaining user credentials
class Database:
    
    def __init__(self, username: str, password: str):
        self.uname = username
        self.passw = password

    #authentication of provided credentials
    def authenticate(self) -> bool:

        try:
            #initialize connection with MySQL
            self.connection = mc.connect(host = "localhost", user = f"{self.uname}", password = f"{self.passw}")

            if (self.connection.is_connected()):
                #initialize cursor object for operation
                self.cursor = self.connection.cursor(buffered = True)
                return True

            else:
                return False

        except:
            return False

    #authentication of existing databases
    def auth_db(self, database: str) -> bool:

        self.cursor.execute("show databases")
        #list of all databases of user
        result = self.cursor.fetchall()

        for db in result:

            if (db[0] == database):
                self.cursor.execute(f"use {database}")
                return True

        return False

    #authentication of existing tables
    def auth_table(self, table: str) -> bool:

        self.cursor.execute("show tables")
        #list of all tables in selected databse
        result = self.cursor.fetchall()

        for data in result:

            if (data[0] = table):
                return True

        return False

'''
PySQL
Devansh Singh, 2021
'''