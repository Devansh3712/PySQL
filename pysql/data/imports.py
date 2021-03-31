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
    import mysql.connector as mc
    import packages.auth as auth

except:
    raise Exception("'imports' module not setup")


class Import:
    """
    class for importing databases & table schemas
    into the database

    :import_database:   ->  if the db name is valid, imports
                            the contents of `.sql` file to
                            the database
                            [returns boolean value]

    :import_table:      ->  if the db name and table name are
                            valid, imports the contents of `.sql`
                            file to the database
                            [returns boolean value]
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
            raise Exception("User could not be authenticated")

    def import_table(self, db: str, path: str) -> bool:
        """
        Imports the input `.sql` file in the
        input table in the given database
        `mysql -u <uname> -p<passwd> <db_name> < <filename>.sql`

        path    ->  path to the `.sql` file
                    (default is current directory)
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
        Imports the input `.sql` file, to the
        input database, executes the command
        `mysql -u <uname> -p<passwd> <db_name> < <filename>.sql`

        path    ->  path to the `.sql` file
                    (default is current directory)
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
