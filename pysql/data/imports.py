"""
module for importing databases
and table schemas as `.sql`
files
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

try:
    import pysql.utils.exceptions as exceptions
    import mysql.connector as mc
    import pysql.packages.auth as auth

except:
    raise exceptions.ModuleSetupError("imports")


class Import:
    """
    class for importing databases & table schemas
    into the database

    Parameters
    ----------
    username: str
        MySQL username of user
    password: str
        MySQL password of user

    Instances
    ---------
    self.uname: str
        username
    self.passw: str
        password
    self.const
        authorization instance
    self.connection
        mysql.connector connection
    self.cursor
        mysql.connector cursor
    """
    def __init__(self, username: str, password: str):

        self.uname = username
        self.passw = password
        # create a `Database` class instance
        self.const = auth.Database(self.uname, self.passw)
        # authenticate data using auth module
        authenticate = self.const.authenticate()

        if (authenticate is True):
            # initialize connection with MySQL server and cursor object for execution of commands
            self.connection = mc.connect(
                host = "localhost",
                user = f"{self.uname}",
                password = f"{self.passw}",
                autocommit = True
            )
            self.cursor = self.connection.cursor(buffered = True)

        else:
            raise exceptions.AuthenticationError()

    def import_table(self, db: str, path: str) -> bool:
        """
        Imports the input SQL file in the
        input table in the given database

        Parameters
        ----------
        db: str
            name of database to import to
        path:
            path of SQL file
        
        Returns
        -------
        bool
            True if table is imported else False
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_db(db)

        try:
            if (authenticate is True):
                if path == "":
                    os.system(f"mysql -u {self.uname} -p{self.passw} {db} < {path}")

                else:
                    os.system(f"mysql -u {self.uname} -p{self.passw} {db} < {path}")

                return True

            else:
                return False

        except:
            return False

    def import_database(self, db: str, path: str) -> bool:
        """
        Imports the input SQL file, to the
        input database

        Parameters
        ----------
        db: str
            name of database to import
        path:
            path of SQL file
        
        Returns
        -------
        bool
            True if database is imported else False
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_db(db)

        try:
            if (authenticate is True):
                if path == "":
                    os.system(f"mysql -u {self.uname} -p{self.passw} {db} < {path}")

                else:
                    os.system(f"mysql -u {self.uname} -p{self.passw} {db} < {path}")

                return True

            else:
                return False

        except:
            return False


"""
PySQL
Devansh Singh, 2021
"""
