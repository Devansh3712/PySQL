"""
module for data-manipulation
language based commands
"""

try:
    import mysql.connector as mc
    import auth

except:
    raise Exception("'dml_commands' module not setup")


class DML:
    """
    class for implementation of Data Manipulation Language
    based commands (select, update, delete, insert)
    """

    def __init__(self, username, password, database, table):

        self.uname = username
        self.passw = password
        self.db = database
        self.table = table
        # create a `Database` class instance
        self.const = auth.Database(self.uname, self.passw, self.db)
        # authenticate data using auth module
        authenticate = self.const.authenticate()

        if (authenticate is True):
            # initialize connection with MySQL server and cursor object for execution of commands
            self.connection = mc.connect(
                host = "localhost",
                user = f"{self.uname}",
                password = f"{self.passw}",
                database = f"{self.db}",
                autocommit = True
            )
            self.cursor = self.connection.cursor(buffered = True)

        else:
            raise Exception("User could not be authenticated")


"""
PySQL
Devansh Singh, 2021
"""