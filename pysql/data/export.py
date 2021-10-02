"""
module for exporting tables &
databases as CSV, JSON
& SQL files
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
    class for exporting tables in JSON & CSV
    format and database in SQL format

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

    def export_table_json(self, db: str, table: str, path: str) -> bool:
        """
        Export the input table as a JSON file

        Parameters
        ----------
        db: str
            name of database to use
        table: str
            name of table to export
        path: str
            path to export table
        
        Returns
        -------
        bool
            True if table is exported else False
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

                file = open(os.path.join(path, f"{table}.csv"), encoding = "utf-8")
                new_file = open(os.path.join(path, f"{table}.json"), "w", encoding = "utf-8")
                reader_obj = csv.DictReader(file)
                # numbering the rows
                key = 1

                # add rows in data dictionary
                for rows in reader_obj:
                    data[key] = rows
                    key += 1

                file.close()
                os.remove(os.path.join(path, f"{table}.csv"))

                new_file.write(json.dumps(data, indent = 4))
                new_file.close()

                return True

            else:
                return False

        except:
            return False

    def export_table_csv(self, db: str, table: str, path: str) -> bool:
        """
        Export the input table as a CSV file

        Parameters
        ----------
        db: str
            name of database to use
        table: str
            name of table to export
        path: str
            path to export table
        
        Returns
        -------
        bool
            True if table is exported else False
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

                file = open(os.path.join(path, f"{table}.csv"), "w", newline = "")
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
        database as JSON files

        Parameters
        ----------
        db: str
            name of database to use
        path: str
            path to export tables
        
        Returns
        -------
        bool
            True if tables are exported else False
        """
        try:
            self.cursor.execute(f"use {db}")
            query = f"show tables"
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            # if <db_name> directory does not exist, create one
            if os.path.isdir(f"{os.path.join(path, db)}") is False:
                if path != "":
                    if platform.system() == "Windows":
                        path_n = path.replace("/", "\\")
                        os.system(f"mkdir {os.path.join(path_n, db)}")

                    else:
                        os.system(f"mkdir {os.path.join(path, db)}")

                else:
                    if platform.system() == "Windows":
                        path = os.path.expanduser("~")
                        os.system(f"mkdir {os.path.join(path, db)}")

                    else:
                        os.system(f"mkdir ~/{db}")

            for tb in result:
                res = Export(self.uname, self.passw).export_table_json(db, tb[0], os.path.join(path, db))

                if res is False:
                    return False

            return True

        except:
            return False

    def export_all_csv(self, db: str, path: str) -> bool:
        """
        Export all tables present in the current
        database as CSV files

        Parameters
        ----------
        db: str
            name of database to use
        path: str
            path to export tables
        
        Returns
        -------
        bool
            True if tables are exported else False
        """
        try:
            self.cursor.execute(f"use {db}")
            query = f"show tables"
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            # if <db_name> directory does not exist, create one
            if os.path.isdir(f"{os.path.join(path, db)}") is False:
                if path != "":
                    if platform.system() == "Windows":
                        path_n = path.replace("/", "\\")
                        os.system(f"mkdir {os.path.join(path_n, db)}")

                    else:
                        os.system(f"mkdir {os.path.join(path, db)}")

                else:
                    if platform.system() == "Windows":
                        path = os.path.expanduser("~")
                        os.system(f"mkdir {os.path.join(path, db)}")

                    else:
                        os.system(f"mkdir ~/{db}")

            for tb in result:
                res = Export(self.uname, self.passw).export_table_csv(db, tb[0], os.path.join(path, db))

                if res is False:
                    return False

            return True

        except:
            return False

    def export_all_sql(self, db: str, path: str) -> bool:
        """
        Export all tables present in the current
        database as SQL files

        Parameters
        ----------
        db: str
            name of database to use
        path: str
            path to export tables
        
        Returns
        -------
        bool
            True if tables are exported else False
        """
        try:
            self.cursor.execute(f"use {db}")
            query = f"show tables"
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            # if <db_name> directory does not exist, create one
            if os.path.isdir(f"{os.path.join(path, db)}") is False:
                if path != "":
                    if platform.system() == "Windows":
                        path_n = path.replace("/", "\\")
                        os.system(f"mkdir {os.path.join(path_n, db)}")

                    else:
                        os.system(f"mkdir {os.path.join(path, db)}")

                else:
                    if platform.system() == "Windows":
                        path = os.path.expanduser("~")
                        os.system(f"mkdir {os.path.join(path, db)}")

                    else:
                        os.system(f"mkdir ~/{db}")

            for tb in result:
                res = Export(self.uname, self.passw).export_table_sql(db, tb[0], os.path.join(path, db))

                if res is False:
                    return False

            return True

        except:
            return False

    def export_database(self, db: str, path: str) -> bool:
        """
        Export the input database in SQL format

        Parameters
        ----------
        db: str
            name of database to export
        path: str
            path to export SQL file
        
        Returns
        -------
        bool
            True if database is exported else False
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_db(db)

        try:
            if (authenticate is True):
                if path == "":
                    os.system(f"mysqldump -u {self.uname} -p{self.passw} {db} > {db}.sql")

                else:
                    PATH = os.path.join(path, f"{db}.sql")
                    os.system(f"mysqldump -u {self.uname} -p{self.passw} {db} > {PATH}")

                return True

            else:
                return False

        except:
            return False

    def export_table_sql(self, db: str, table: str, path: str) -> bool:
        """
        Export the input table's schema in SQL format

        Parameters
        ----------
        db: str
            name of database to use
        table: str
            name of table to export
        path: str
            path to export SQL file
        
        Returns
        -------
        bool
            True if table is exported else False
        """
        # authenticate whether the table exists or not
        authenticate_1 = self.const.auth_db(db)
        authenticate_2 = self.const.auth_table(db, table)

        try:
            if (authenticate_1 is True and authenticate_2 is True):
                if path == "":
                    os.system(f"mysqldump -u {self.uname} -p{self.passw} {db} {table} > {db}.{table}.sql")

                else:
                    PATH = os.path.join(path, f"{db}.{table}.sql")
                    os.system(f"mysqldump -u {self.uname} -p{self.passw} {db} {table} > {PATH}")

                return True

            else:
                return False

        except:
            return False


"""
PySQL
Devansh Singh, 2021
"""
