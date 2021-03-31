"""
module for data-manipulation
language based commands
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

try:
    import mysql.connector as mc
    import tabulate
    import csv
    import packages.auth as auth

except:
    raise Exception("'dml_commands' module not setup")


class DML:
    """
    class for implementation of Data Manipulation Language
    based commands (select, update, delete, insert)

    :select:        ->  if the `table` name is valid, shows
                        the table with value of selected columns
                        with given arguments, formatted with tabulate
                        [returns formatted table else False]

    :insert:        ->  if the `table` name is valid, inserts the
                        input value (single row) into the table
                        [returns boolean value]

    :insert_file:   ->  if the `table` name is valid, inserts
                        the values in the CSV file into the table
                        [returns boolean value]

    :update:        ->  if the `table` name is valid, updates
                        the input columns for the given
                        arguments
                        [returns boolean value]

    :delete:        ->  if the `table` name is valid, deletes
                        the input columns
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

    def select(self, db: str, table: str, columns: str, args: str):
        """
        Shows the selected components of the current
        table, executing the SQL query
        `select <columns> from <table_name> where <args>`

        columns ->  columns to be chosen, default is `*` 
                    (all columns)
        args    ->  arguments for the select query, default
                    is "" <NULL>
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                self.cursor.execute(f"use {db}")

                # if no arguments are provided for selection
                if (args == ""):

                    if (columns == ""):
                        columns = "*"

                    query = f"select {columns} from {table}"
                    self.cursor.execute(query)
                    select_result = self.cursor.fetchall()
                    # provides column names in the input table
                    table_columns = self.cursor.column_names

                    result = tabulate.tabulate(
                        select_result,
                        headers = list(table_columns),
                        tablefmt = "psql"
                    )
                    return result

                else:

                    if (columns == ""):
                        columns = "*"

                    query = ""
                    # if query has an aggregrate command
                    if "sum" in args or "min" in args or "max" in args or "avg" in args or "count" in args:
                        query = f"select {columns} from {table} having {args}"
                    # if the query has order by/ group by clause
                    elif args.startswith("group by") or args.startswith("order by"):
                        query = f"select {columns} from {table} {args}"

                    else:
                        query = f"select {columns} from {table} where {args}"

                    self.cursor.execute(query)
                    select_result = self.cursor.fetchall()
                    # provides column names in the input table
                    table_columns = self.cursor.column_names

                    result = tabulate.tabulate(
                        select_result,
                        headers = list(table_columns),
                        tablefmt = "psql"
                    )
                    return result

            else:
                return False

        except:
            return False

    def insert(self, db: str, table: str, args: str) -> bool:
        """
        Inserts a single row into the selected
        table, executing the SQL query
        `insert into <tb_name> values (<args>)`

        args    ->  comma separated values to
                    to be entered in the table
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                self.cursor.execute(f"use {db}")

                # create list of values to be inserted
                args = args.split(",")
                self.cursor.execute(f"select * from {table}")
                # get column names
                columns = self.cursor.column_names

                # number of columns and number of values inserted should be equal
                if len(args) != len(columns):
                    return False

                else:

                    args = [x.strip(" ") for x in args]

                    if len(args) == 1:
                        query = f"insert into {table} values ({str(args[0])})"
                        self.cursor.execute(query)

                    else:
                        query = f"insert into {table} values {tuple(args)}"
                        self.cursor.execute(query)

                    return True
            else:
                return False

        except:
            return False

    def insert_file(self, db: str, table: str, file_name: str) -> bool:
        """
        Inserts values into the input table from
        a comma separated value (CSV) file, uses the
        :insert: function of `DML` class
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                self.cursor.execute(f"use {db}")

                # check if CSV file exists
                if os.path.exists(file_name):

                    file = open(file_name, "r")
                    # create reader object for CSV file
                    reader_obj = csv.reader(file)
                    # read contents as a list of lists
                    content = list(reader_obj)
                    file.close()

                    for record in content:
                        row = ",".join(map(str, record))
                        # call the :insert: function
                        result = DML(self.uname, self.passw).insert(db, table, row)

                        if result is False:
                            return False

                    return True

                else:
                    return False

            else:
                return False

        except:
            return False

    def update(self, db: str, table: str, columns: str, args: str) -> bool:
        """
        Update values in the input table of
        selected columns, executing the SQL query
        `update <tb_name> set <columns> where <args>`

        columns ->  columns whose value has to be
                    updated
        args    ->  rows of which values has to be
                    updated
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                self.cursor.execute(f"use {db}")

                # if no arguments are given
                if args == "":

                    columns = columns.strip(" ")
                    query = f"update {table} set {columns}"
                    self.cursor.execute(query)

                    return True

                else:

                    args = args.strip(" ")
                    columns = columns.strip(" ")
                    query = f"update {table} set {columns} where {args}"
                    self.cursor.execute(query)

                    return True

            else:
                return False

        except:
            return False

    def delete(self, db: str, table: str, column: str) -> bool:
        """
        Delete values in the input table of
        selected columns, executing the SQL query
        `delete from <tb_name> where <columns>`

        column  ->  column whose value has to be
                    deleted
        """        
        # authenticate whether the table exists or not
        authenticate = self.const.auth_table(db, table)

        try:
            if (authenticate is True):

                self.cursor.execute(f"use {db}")

                # if no arguments are given
                if column == "":

                    # deletes all records in table
                    query = f"delete from {table}"
                    self.cursor.execute(query)

                    return True

                else:

                    column = column.strip(" ")
                    query = f"delete from {table} where {column}"
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
