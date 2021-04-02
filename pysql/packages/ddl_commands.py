"""
module for data-definition
language based commands
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

try:
    import mysql.connector as mc
    import tabulate
    import packages.auth as auth

except:
    raise Exception("'ddl_commands' module not setup")


class DDL:
    """
    class for implementation of Data Definition Language
    based commands (create, drop, alter)

    :show_databases:    ->  returns all available databases
                            in the local MySQL server
                            [returns formatted result else False]

    :show_tables:       ->  returns all available tables in the
                            current database
                            [returns formatted result else False]

    :create_database:   ->  create a new database in the
                            MySQL server
                            [returns boolean value]

    :use_database:      ->  use a database present in the
                            MySQL server
                            [returns boolean value]

    :drop_database:     ->  if the database name is valid,
                            deleting the database from server
                            [returns boolean value]

    :create_table:      ->  takes comma separated string arguments,
                            converting them into SQL statements and
                            creating a table in the chosen database
                            [returns boolean value]

    :drop_table:        ->  if the table name is valid,
                            deletes the table from chosen database
                            [returns boolean value]

    :truncate_table:    ->  delete all the data in the provided table
                            without deleting the table
                            [returns boolean value]

    :desc_table:        ->  if the table name is valid, returns
                            the structure of the provided table,
                            formatted using tabulate
                            [returns formatted table else returns False]

    :alter_table:       ->  if the table name is valid, and the column
                            name is authenticated, alters the structure
                            of the input table in the current database
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

    def show_databases(self):
        """
        Returns all the databases in the
        local MySQL server, formatted using
        tabulate

        executes the SQL query `show databases`
        """
        try:
            query = "show databases"
            self.cursor.execute(query)
            db_result = self.cursor.fetchall()

            result = tabulate.tabulate(
                db_result,
                headers = ["Databases"],
                tablefmt = "psql"
            )
            return result

        except:
            return False

    def create_database(self, database: str) -> bool:
        """
        Creates a new database in the MySQL server of the
        local machine, executing the SQL query
        `create database <db_name>`
        """
        try:
            query = f"create database {database}"
            self.cursor.execute(query)
            return True

        except:
            return False

    def use_database(self, database: str) -> bool:
        """
        Use the input database of the local MySQL
        server, if it exists, executing the SQL query
        `use <db_name>`
        """
        # authenticate whether database exists or not
        authenticate = self.const.auth_db(database)

        try:
            if (authenticate is True):

                query = f"use {database}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def drop_database(self, database: str) -> bool:
        """
        Drops/deletes the input database in the MySQL Server,
        if it exists and is valid, executing the SQL query 
        `drop database <db_name>`
        """
        # authenticate whether database exists or not
        authenticate = self.const.auth_db(database)

        try:
            if (authenticate is True):

                query = f"drop database {database}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def show_tables(self):
        """
        Returns all the tables in the
        current database, formatted using
        tabulate

        executes the SQL query `show tables`
        """
        try:
            query = "show tables"
            self.cursor.execute(query)
            db_result = self.cursor.fetchall()

            query = "select database()"
            self.cursor.execute(query)
            db = self.cursor.fetchone()

            result = tabulate.tabulate(
                db_result,
                headers = [f"Tables_in_{db[0]}"],
                tablefmt = "psql"
            )
            return result

        except:
            return False

    def create_table(self, table: str, args: list) -> bool:
        """
        Creates a table in the current database with 
        provided arguments in the form of SQL statement,
        executing the SQL query `create table <table_name> (data)`

        table   ->  name of table to be created
        args    ->  provide column names and datatypes
        """
        try:
            # statement with column parameters for MySQL table
            statement = ""
            for num in range (len(args)):

                if (num == len(args) - 1):
                    statement += args[num]

                else:
                    statement += args[num] + ", "

            query = f"create table {table} ({statement})"
            self.cursor.execute(query)
            return True

        except:
            return False

    def drop_table(self, db: str, table: str) -> bool:
        """
        Drops/deletes the input table in the current
        database if table exists and is valid,
        executing the SQL query `drop table <table_name>`
        """
        # authenticate whether table name exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                self.cursor.execute(f"use {db}")
                query = f"drop table {table}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def truncate_table(self, db: str, table: str) -> bool:
        """
        Deletes the data of the input table, if the
        table exists and is valid, executing the
        SQL query `truncate table <table_name>`
        """
        # authenticate whether table name exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                self.cursor.execute(f"use {db}")
                query = f"truncate table {table}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def desc_table(self, db: str, table: str):
        """
        Returns the structure of the input table,
        formatted using `tabulate` module if the
        table exists and is valid

        representation of the SQL query `desc <table_name>`
        """
        # authenticate whether table name exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                self.cursor.execute(f"use {db}")
                query = f"desc {table}"
                self.cursor.execute(query)
                desc_result = self.cursor.fetchall()

                # tabulate the table structure
                result = tabulate.tabulate(
                    desc_result,
                    headers = [
                        'Field',
                        'Type',
                        'Null',
                        'Key',
                        'Default',
                        'Extra'
                    ],
                    tablefmt = "psql"
                )
                return result

            else:
                return False

        except:
            return False

    def alter_table(self, db: str, table: str, args: list) -> bool:
        """
        Alters the content of the input table, if
        the table exists and the column name is valid

        option for alter table are `add`, `modify column`
        and `drop_column`, using the `Alter` class
        """
        # authenticate whether table name exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                # create `Alter` class instance
                const = Alter(self.uname, self.passw, db, table)
                args[1] = args[1].lstrip(" ")

                if (args[0] == "add"):
                    if (const.add_column(args[1]) is True):
                        return True

                    else:
                        return False

                elif (args[0] == "modify"):
                    if (const.modify_column(args[1]) is True):
                        return True

                    else:
                        return False

                elif (args[0] == "drop"):
                    if (const.drop_column(args[1]) is True):
                        return True

                    else:
                        return False

                else:
                    return False

            else:
                return False

        except:
            return False


class Alter:
    """
    class for implementation of variations of `DDL.alter_table`
    command (add, modify column, drop column)

    :add_column:    ->  adds the input column in the current table,
                        if the name and the type of column are valid
                        [returns boolean value]

    :drop_column:   ->  drops/deletes the input column from the
                        current table if the name of the column is valid
                        [returns boolean value]

    :modify_column: ->  modifies the input column in the current
                        table if the name and the type of the
                        column are valid
                        [returns boolean value]
    """

    def __init__(self, username: str, password: str, database: str, table: str):

        self.uname = username
        self.passw = password
        self.table = table
        self.db = database
        # create a `Database` class instance
        self.const = auth.Database(self.uname, self.passw)

        self.connection = mc.connect(
            host = "localhost",
            user = f"{self.uname}",
            password = f"{self.passw}",
            database = f"{self.db}",
            autocommit = True
        )
        self.cursor = self.connection.cursor(buffered = True)

    def add_column(self, column: str) -> bool:
        """
        Adds the input column into the current
        table if the column name is valid, using
        the SQL query `alter table <table_name> add <column_name>`
        """
        try:
            query = f"alter table {self.table} add {column}"
            self.cursor.execute(query)
            return True

        except:
            return False

    def drop_column(self, column: str) -> bool:
        """
        Drops/deletes the input column from the current
        table if the column name is valid, using the
        SQL query `alter table <table_name> drop column <column_name>` 
        """
        # authenticate whether column details exist in table or not
        authenticate = self.const.auth_table_columns(self.db, self.table, column)

        try:
            if (authenticate is True):

                query = f"alter table {self.table} drop column {column}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def modify_column(self, column: str) -> bool:
        """
        Modifies the input column name along with input
        column value type if column name is valid, using
        the SQL query `alter table <table_name> modify column <column_name> <value>`
        """
        auth_column = column.split(' ')
        # authenticate whether column details exist in table or not
        authenticate = self.const.auth_table_columns(self.db, self.table, auth_column[0])

        try:
            if (authenticate is True):

                query = f"alter table {self.table} modify column {column}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False


"""
PySQL
Devansh Singh, 2021
"""
