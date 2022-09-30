import os
import sys

# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import csv
from typing import Union

import mysql.connector as mc
import tabulate

import pysql.utils.exceptions as exceptions
import pysql.packages.auth as auth


class DML:
    """Class for implementation of commands based on
    Data Manipulation Language (SELECT, UPDATE, DELETE, INSERT)

    Parameters
    ----------
    username: str
        MySQL username
    password: str
        MySQL password
    """

    def __init__(self, username: str, password: str):
        self.uname = username
        self.passw = password
        # create a `Database` class instance
        self._auth = auth.Database(self.uname, self.passw)
        # authenticate data using auth module
        authenticate = self._auth.authenticate()
        if authenticate is True:
            # initialize connection with MySQL server and cursor object for execution of commands
            self.connection = mc.connect(
                host="localhost", user=self.uname, password=self.passw, autocommit=True
            )
            self.cursor = self.connection.cursor(buffered=True)

        else:
            raise exceptions.AuthenticationError()

    def select(self, db: str, table: str, columns: str, args: str) -> Union[str, bool]:
        """Shows the selected components of the current table

        Parameters
        ----------
        db : str
            name of database to use
        table : str
            name of table to select
        columns : str
            specifc columns to choose (if any)
        args : str
            specific arguments (if any)

        Returns
        -------
        str
            selected columns of table
        bool
            False if any error occurs
        """
        # authenticate whether the table exists or not
        authenticate = self._auth.auth_table(db, table)
        try:
            if authenticate is True:
                self.cursor.execute(f"use {db}")
                # if no arguments are provided for selection
                if args == "":
                    if columns == "":
                        columns = "*"

                    query = f"select {columns} from {table}"
                    self.cursor.execute(query)
                    select_result = self.cursor.fetchall()
                    # provides column names in the input table
                    table_columns = self.cursor.column_names
                    result = tabulate.tabulate(
                        select_result, headers=list(table_columns), tablefmt="psql"
                    )
                    return result

                else:
                    if columns == "":
                        columns = "*"
                    query = None
                    # if query has an aggregrate command
                    if (
                        "sum" in args
                        or "min" in args
                        or "max" in args
                        or "avg" in args
                        or "count" in args
                    ):
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
                        select_result, headers=list(table_columns), tablefmt="psql"
                    )
                    return result

            else:
                return False

        except:
            return False

    def insert(self, db: str, table: str, args: str) -> bool:
        """Inserts a single row into the selected table

        Parameters
        ----------
        db : str
            name of database to use
        table : str
            name of table to insert into
        args : str
            specific arguments (if any)

        Returns
        -------
        bool
            True if data is inserted else False
        """
        # authenticate whether the table exists or not
        authenticate = self._auth.auth_table(db, table)
        try:
            if authenticate is True:
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
        """Inserts values into the input table from
        a comma separated value (CSV) file

        Parameters
        ----------
        db : str
            name of database to use
        table : str
            name of table to insert into
        file_name : str
            path to file containing data

        Returns
        -------
        bool
            True if data is inserted else False
        """
        # authenticate whether the table exists or not
        authenticate = self._auth.auth_table(db, table)
        try:
            if authenticate is True:
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
        """Update values in the input table of
        selected columns

        Parameters
        ----------
        db : str
            name of database to use
        table : str
            name of table to update
        columns : str
            specifc columns to update (if any)
        args : str
            specific arguments (if any)

        Returns
        -------
        bool
            True if data is updated else False
        """
        # authenticate whether the table exists or not
        authenticate = self._auth.auth_table(db, table)
        try:
            if authenticate is True:
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
        """Delete values in the input table of
        selected columns

        Parameters
        ----------
        db : str
            name of database to use
        table : str
            name of table to delete from
        args : str
            specific arguments (if any)

        Returns
        -------
        bool
            True if data is deleted else False
        """
        # authenticate whether the table exists or not
        authenticate = self._auth.auth_table(db, table)
        try:
            if authenticate is True:
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
