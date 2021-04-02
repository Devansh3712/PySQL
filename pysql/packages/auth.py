"""
module for user and data
authentication
"""

try:
    import mysql.connector as mc

except:
    raise Exception("'auth' module not setup")


class Database:
    """
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
    """

    def __init__(self, username: str, password: str):
        """
        Initialize connection and cursor object as `NoneType`
        so that its value can change when authenticate() is called
        """
        self.uname = username
        self.passw = password
        Database.connection = None
        Database.cursor = None

    def authenticate(self) -> bool:
        """
        Connect to the MySQL server on the local machine
        with the initialized `self.uname` and `self.passw`

        if username or password is wrong/invalid or it
        is unable to connect to MySQL, returns False

        else if connection is made, a cursor object is
        initialized which is used to execute SQL commands
        """
        try:
            # initialize connection with MySQL
            Database.connection = mc.connect(
                host = "localhost",
                user = f"{self.uname}",
                password = f"{self.passw}",
                autocommit = True
            )

            if (Database.connection.is_connected()):
                # initialize cursor object for execution of commands
                Database.cursor = Database.connection.cursor(buffered = True)
                return True

            else:
                return False

        except:
            return False

    def auth_db(self, database: str) -> bool:
        """
        Check whether the provided database exists
        or not in the MySQL server

        it generates a list of tuples containing all
        databases in MySQL server, and if input
        database is in the list, returns True
        """
        authenticate = Database(self.uname, self.passw).authenticate()

        try:
            if (authenticate is True):

                Database.cursor.execute("show databases")
                # list of all databases of user
                result = Database.cursor.fetchall()

                for db in result:

                    if (db[0] == database):
                        return True

                return False

            else:
                return False

        except:
            return False

    def auth_table(self, db: str, table: str) -> bool:
        """
        Check whether the provided table exists
        or not in the selected database

        it generates a list of tuples containing all
        tables in the selected database, and if input
        table is in the list, returns True
        """
        authenticate = Database(self.uname, self.passw).authenticate()

        try:
            if (authenticate is True):

                Database.cursor.execute(f"use {db}")
                Database.cursor.execute("show tables")
                # list of all tables in selected database
                result = Database.cursor.fetchall()

                for data in result:

                    if (data[0] == table):
                        return True

                return False

            else:
                return False

        except:
            return False

    def auth_table_columns(self, db: str, table: str, query: str) -> bool:
        """
        Check whether the provided table has the
        given column as a parameter and its
        description matches

        it generates a list of tuples containing
        structure of the table, and if the column name
        and type match, returns True
        """
        authenticate = Database(self.uname, self.passw).authenticate()

        try:
            if (authenticate is True):

                # split column name and type of column
                query = query.split(' ')
                Database.cursor.execute(f"use {db}")
                Database.cursor.execute(f"select * from {table}")
                # contains description of all columns in the table
                result = Database.cursor.description

                for column in result:

                    if (column[0].lower() == query[0].lower()):
                        return True

                return False

            else:
                return False

        except:
            return False


"""
PySQL
Devansh Singh, 2021
"""
