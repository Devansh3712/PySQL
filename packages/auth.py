'''
module for user and data
authentication
'''

try:
    import mysql.connector as mc

except:
    raise Exception("'auth' module not setup")

class Database:

    '''
    class for maintaining and authenticating user,
    database and table credentials

    :authenticate:      ->  authenticate the username, password
                            and selected database of MySQL user
                            [returns boolean value]

    :auth_db:           ->  authenticate whether the input database
                            exists or in MySQL server
                            [returns boolean value]

    :auth_table:        ->  authenticate whether the input table
                            exists in the selected database
                            [returns boolean value]

    :auth_table_colums: ->  authenticate whether the input column
                            and datatype exist in the selected
                            table
                            [returns boolean value]
    '''

    def __init__(self, username: str, password: str, database: str):

        '''
        initialize connection and cursor object as `NoneType`
        so that its value can change when authenticate() is called
        '''

        self.uname = username
        self.passw = password
        self.db = database
        Database.connection = None
        Database.cursor = None

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
            Database.connection = mc.connect(
                host = "localhost",
                user = f"{self.uname}",
                password = f"{self.passw}",
                database = f"{self.db}",
                autocommit = True
            )

            if (Database.connection.is_connected()):
                #initialize cursor object for execution of commands
                Database.cursor = Database.connection.cursor(buffered = True)
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

        authenticate = Database(self.uname, self.passw, self.db).authenticate()
        if (authenticate == True):

            Database.cursor.execute("show databases")
            #list of all databases of user
            result = Database.cursor.fetchall()

            for db in result:

                if (db[0] == database):
                    return True

            return False

        else:
            return False

    def auth_table(self, table: str) -> bool:

        '''
        check whether the provided table exists
        or not in the selected database

        it generates a list of tuples containing all
        tables in the selected database, and if input
        table is in the list, returns True
        '''

        authenticate = Database(self.uname, self.passw, self.db).authenticate()
        if (authenticate == True):

            Database.cursor.execute("show tables")
            #list of all tables in selected database
            result = Database.cursor.fetchall()

            for data in result:

                if (data[0] == table):
                    return True

            return False

        else:
            return False

    def auth_table_columns(self, table: str, query: str) -> bool:

        '''
        check whether the provided table has the
        given column as a parameter and its
        description matches

        it generates a list of tuples containing
        structure of the table, and if the column name
        and type match, returns True
        '''

        authenticate = Database(self.uname, self.passw, self.db).authenticate()
        if (authenticate == True):

            type_dict = {
                0: 'DECIMAL',
                1: 'TINY',
                2: 'SHORT',
                3: 'LONG',
                4: 'FLOAT',
                5: 'DOUBLE',
                6: 'NULL',
                7: 'TIMESTAMP',
                8: 'LONGLONG',
                9: 'INT24',
                10: 'DATE',
                11: 'TIME',
                12: 'DATETIME',
                13: 'YEAR',
                14: 'NEWDATE',
                15: 'VARCHAR',
                16: 'BIT',
                246: 'NEWDECIMAL',
                247: 'INTERVAL',
                248: 'SET',
                249: 'TINY_BLOB',
                250: 'MEDIUM_BLOB',
                251: 'LONG_BLOB',
                252: 'BLOB',
                253: 'VAR_STRING',
                254: 'STRING',
                255: 'GEOMETRY'
            }

            #split column name and type of column
            query = query.split(' ')
            Database.cursor.execute("select * from {table}")
            #contains description of all columns in the table
            result = Database.cursor.description

            for column in result:

                if (column[0].lower() == query[0].lower()):

                    try:
                        #if column type specifies size
                        query[1] = query[1].split('(')[0]

                    except:
                        pass

                    if (type_dict[column[1]].lower() == query[1].lower()):
                        return True
            
            return False
        
        else:
            return False

'''
PySQL
Devansh Singh, 2021
'''