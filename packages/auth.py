'''
module for user and data
authentication
'''
try:
    import mysql.connector as mc

except:
    print("'auth.py' module not setup")
    exit()

class Database:

    '''
    class for maintaining and authencating user,
    database and table credentials

    :authenticate:  ->  authenticate the username and password
                        of MySQL user
    :auth_db:       ->  authenticate whether the input database
                        exists or in MySQL server
    :auth_table:    ->  authenticate whether the input table
                        exists in the selected database
    '''
    
    def __init__(self, username: str, password: str):
        self.uname = username
        self.passw = password

    def authenticate(self) -> bool:

        '''
        connect to the MySQL server on the local machine
        with the initialized `self.uname` and `self.passw`

        if username or password is wrong/invalid or it
        is unable to connect to MySQL, returns False

        else if connection is made, a cursor object is
        initialized which is used to execute SQL commands
        '''

        try:
            #initialize connection with MySQL
            self.connection = mc.connect(host = "localhost", user = f"{self.uname}", password = f"{self.passw}")

            if (self.connection.is_connected()):
                #initialize cursor object for execution
                self.cursor = self.connection.cursor(buffered = True)
                return True

            else:
                return False

        except:
            return False

    def auth_db(self, database: str) -> bool:

        '''
        check whether the provided database exists
        or not in the MySQL server

        it generates a list of tuples containing all
        databases in MySQL server, and if input
        database is in the list, returns True
        '''

        self.cursor.execute("show databases")
        #list of all databases of user
        result = self.cursor.fetchall()

        for db in result:

            if (db[0] == database):
                self.cursor.execute(f"use {database}")
                return True

        return False

    def auth_table(self, table: str) -> bool:

        '''
        check whether the provided table exists
        or not in the selected database

        it generates a list of tuples containing all
        tables in the selected database, and if input
        table is in the list, returns True
        '''

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