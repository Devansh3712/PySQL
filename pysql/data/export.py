"""
module for exporting tables &
databases as `.txt`, `.csv`
& `.sql` files
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

try:
    import pysql.utils.exceptions as exceptions
    import mysql.connector as mc
    import csv
    import json
    import platform
    import pysql.packages.auth as auth

except:
    raise exceptions.ModuleSetupError("export")


class Export:
    """
    class for exporting tables in `.txt` & `.csv`
    format and database in `.sql` format

    :export_table_json: ->  if the `table` name is valid, exports
                            the table as `.json` file
                            [returns boolean value]

    :export_table_csv:  ->  if the `table` name is valid, exports
                            the table as `.csv` file, formatted
                            using tabulate
                            [returns boolean value]

    :export_all_json:   ->  exports all the tables present in the
                            current database in <db_name> directory
                            as `.json` files, using :export_table_json:
                            function
                            [returns boolean value]

    :export_all_csv:    ->  exports all the tables present in the
                            current database in <db_name> directory
                            as `.csv` files, using :export_table_txt:
                            function
                            [returns boolean value]

    :export_all_sql:    ->  exports all the tables' schema present in the
                            current database in <db_name> directory
                            as `.sql` files, using :export_table_sql:
                            function
                            [returns boolean value]

    :export_database:   ->  exports the input database in `.sql` format,
                            if the database exists
                            [returns boolean value]

    :export_table_sql:  ->  exports the input table's schema in `.sql`
                            format, if the db & table exists
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
            raise exceptions.AuthenticationError()

    def export_table_json(self, db: str, table: str, path: str) -> bool:
        """
        Export the input table as a `.json` file,
        using the :export_table_csv: function

        path    ->  path where file has to be exported
                    (default is current directory)
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                if path == "":
                    path = os.path.expanduser("~")
                    path = path.replace("\\", "/")

                # export a csv file of table
                Export(self.uname, self.passw).export_table_csv(db, table, f"{path}")
                data = {}

                file = open(f"{path}/{table}.csv", encoding = "utf-8")
                new_file = open(f"{path}/{table}.json", "w", encoding = "utf-8")
                reader_obj = csv.DictReader(file)
                # numbering the rows
                key = 1

                # add rows in data dictionary
                for rows in reader_obj:
                    data[key] = rows
                    key += 1

                file.close()
                os.remove(f"{path}/{table}.csv")

                new_file.write(json.dumps(data, indent = 4))
                new_file.close()

                return True

            else:
                return False

        except:
            return False

    def export_table_csv(self, db: str, table: str, path: str) -> bool:
        """
        Export the input table as a `.csv` file,
        with result of SQL query
        `select * from <tb_name>`

        path    ->  path where file has to be exported
                    (default is current directory)
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                self.cursor.execute(f"use {db}")
                query = f"select * from {table}"
                self.cursor.execute(query)
                select_result = self.cursor.fetchall()
                # provides column names in the input table
                table_columns = self.cursor.column_names

                if path == "":
                    path = os.path.expanduser("~")
                    path = path.replace("\\", "/")

                file = open(f"{path}/{table}.csv", "w", newline = "")
                writer_obj = csv.writer(file)
                writer_obj.writerow(list(table_columns))

                for row in select_result:
                    writer_obj.writerow(list(row))

                file.close()

                return True

            else:
                return False

        except:
            return False

    def export_all_json(self, db: str, path: str) -> bool:
        """
        Export all tables present in the current
        database as `.json` files, using the
        command :export_table_json:

        path    ->  path where file has to be exported
                    (default is current directory)
        """
        try:
            self.cursor.execute(f"use {db}")
            query = f"show tables"
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            # if <db_name> directory does not exist, create one
            if os.path.isdir(f"{path}/{db}") is False:

                if path != "":

                    if platform.system() == "Windows":
                        path_n = path.replace("/", "\\")
                        os.system(f"mkdir {path_n}\{db}")

                    else:
                        os.system(f"mkdir {path}/{db}")

                else:

                    if platform.system() == "Windows":
                        path = os.path.expanduser("~")
                        os.system(f"mkdir {path}\{db}")

                    else:
                        os.system(f"mkdir ~/{db}")

            for tb in result:
                res = Export(self.uname, self.passw).export_table_json(db, tb[0], f"{path}/{db}")

                if res is False:
                    return False

            return True

        except:
            return False

    def export_all_csv(self, db: str, path: str) -> bool:
        """
        Export all tables present in the current
        database as `.csv` files, using the
        command :export_table_txt:

        path    ->  path where file has to be exported
                    (default is current directory)
        """
        try:
            self.cursor.execute(f"use {db}")
            query = f"show tables"
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            # if <db_name> directory does not exist, create one
            if os.path.isdir(f"{path}/{db}") is False:

                if path != "":

                    if platform.system() == "Windows":
                        path_n = path.replace("/", "\\")
                        os.system(f"mkdir {path_n}\{db}")

                    else:
                        os.system(f"mkdir {path}/{db}")

                else:

                    if platform.system() == "Windows":
                        path = os.path.expanduser("~")
                        os.system(f"mkdir {path}\{db}")

                    else:
                        os.system(f"mkdir ~/{db}")

            for tb in result:
                res = Export(self.uname, self.passw).export_table_csv(db, tb[0], f"{path}/{db}")

                if res is False:
                    return False

            return True

        except:
            return False

    def export_all_sql(self, db: str, path: str) -> bool:
        """
        Export all tables' schema present in the current
        database as `.sql` files, using the
        command :export_table_sql:

        path    ->  path where file has to be exported
                    (default is current directory)
        """
        try:
            self.cursor.execute(f"use {db}")
            query = f"show tables"
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            # if <db_name> directory does not exist, create one
            if os.path.isdir(f"{path}/{db}") is False:

                if path != "":

                    if platform.system() == "Windows":
                        path_n = path.replace("/", "\\")
                        os.system(f"mkdir {path_n}\{db}")

                    else:
                        os.system(f"mkdir {path}/{db}")

                else:

                    if platform.system() == "Windows":
                        path = os.path.expanduser("~")
                        os.system(f"mkdir {path}\{db}")

                    else:
                        os.system(f"mkdir ~/{db}")

            for tb in result:
                res = Export(self.uname, self.passw).export_table_sql(db, tb[0], f"{path}/{db}")

                if res is False:
                    return False

            return True

        except:
            return False

    def export_database(self, db: str, path: str) -> bool:
        """
        Export the input database in `.sql` format,
        executes the command
        `mysqldump -u <uname> -p<passwd> <db_name> > <filename>.sql`

        path    ->  path where file has to be exported
                    (default is current directory)
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_db(db)

        try:
            if (authenticate is True):

                if path == "":
                    os.system(f"mysqldump -u {self.uname} -p{self.passw} {db} > {db}.sql")

                else:
                    os.system(f"mysqldump -u {self.uname} -p{self.passw} {db} > {path}/{db}.sql")

                return True

            else:
                return False

        except:
            return False

    def export_table_sql(self, db: str, table: str, path: str) -> bool:
        """
        Export the input table's schema in
        `.sql` format, executes the command
        `mysqldump -u <uname> -p<passwd> <db_name> <tb_name> > <filename>.sql`

        path    ->  path where file has to be exported
                    (default is current directory)
        """
        # authenticate whether the table exists or not
        authenticate_1 = self.const.auth_db(db)
        authenticate_2 = self.const.auth_table(db, table)

        try:
            if (authenticate_1 is True and authenticate_2 is True):

                if path == "":
                    os.system(f"mysqldump -u {self.uname} -p{self.passw} {db} {table} > {db}.{table}.sql")

                else:
                    os.system(f"mysqldump -u {self.uname} -p{self.passw} {db} {table} > {path}/{db}.{table}.sql")

                return True

            else:
                return False

        except:
            return False


"""
PySQL
Devansh Singh, 2021
"""
