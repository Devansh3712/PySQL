"""
MIT License

Copyright (c) 2021 Devansh Singh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import pysql.packages.auth as auth
import mysql.connector as mc
import tabulate
from typing import Union, List

class DDL:
    """Class for implementation of commands based on
    Data Definition Language (CREATE, DROP, ALTER)

    Attributes
    ----------
    username : str
        local MySQL server username
    password : str
        local MySQL server password

    Methods
    -------
    show_databases
        show all local databases
    create_database
        create a new database
    drop_database
        delete a database
    show_tables
        show all tables of a database
    create_table
        create a new table
    drop_table
        delete an existing table
    truncate_table
        truncate table data
    desc_table
        show table structure
    alter_table
        alter table structure
    """

    def __init__(self, username: str, password: str):
        self.uname = username
        self.passw = password
        # create a `Database` class instance
        self._auth = auth.Database(self.uname, self.passw)
        # authenticate data using auth module
        authenticate = self._auth.authenticate()
        if authenticate is True:
            # initialize connection with MySQL server
            self.connection = mc.connect(
                host = "localhost",
                user = self.uname,
                password = self.passw,
                autocommit = True
            )
            # initialize cursor to communicate with server
            self.cursor = self.connection.cursor(buffered = True)

        else:
            raise exceptions.AuthenticationError()

    def show_databases(self) -> Union[str, bool]:
        """Returns all the databases in the local MySQL server,
        formatted using tabulate

        Returns
        -------
        str
            databases in local machine
        bool
            False if any error occurs
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
        """Creates a new database in the MySQL server of the
        local machine

        Parameters
        ----------
        database : str
            name of the database to be created
        
        Returns
        -------
        bool
            True if database is created else False
        """
        try:
            query = f"create database {database}"
            self.cursor.execute(query)
            return True

        except:
            return False

    def use_database(self, database: str) -> bool:
        """Connect to the input database of the local MySQL
        server

        Parameters
        ----------
        database : str
            name of the database to be created
        
        Returns
        -------
        bool
            True if connection is made else False
        """
        # authenticate whether database exists or not
        authenticate = self._auth.auth_db(database)
        try:
            if authenticate is True:
                query = f"use {database}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def drop_database(self, database: str) -> bool:
        """Deletes the input database in the MySQL Server

        Parameters
        ----------
        database : str
            name of the database to be created
        
        Returns
        -------
        bool
            True if database is deleted else False
        """
        # authenticate whether database exists or not
        authenticate = self._auth.auth_db(database)
        try:
            if authenticate is True:
                query = f"drop database {database}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def show_tables(self, database: str) -> Union[str, bool]:
        """Returns all the tables in the current database,
        formatted using tabulate

        Parameters
        ----------
        database : str
            name of the database to be used

        Returns
        -------
        str
            tables in the current database
        bool
            False if any error occurs
        """
        # authenticate whether database exists or not
        authenticate = self._auth.auth_db(database)
        try:
            if authenticate is True:
                self.cursor.execute(f"use {database}")
                query = "show tables"
                self.cursor.execute(query)
                db_result = self.cursor.fetchall()

                result = tabulate.tabulate(
                    db_result,
                    headers = [f"Tables_in_{database}"],
                    tablefmt = "psql"
                )
                return result
            
            else:
                False

        except:
            return False

    def create_table(self, db: str, table: str, args: List[str]) -> bool:
        """Creates a table in the current database with provided
        arguments in the form of SQL statements

        Parameters
        ----------
        db : str
            name of the database to connect
        table : str
            name of the table to create
        args : list
            table description
        
        Returns
        -------
        bool
            True if table is created else False
        """
        # authenticate whether database exists or not
        authenticate = self._auth.auth_db(db)
        try:
            if authenticate is True:
                self.cursor.execute(f"use {db}")
                # statement with column parameters for MySQL table
                statement = ", ".join(args)
                query = f"create table {table} ({statement})"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def drop_table(self, db: str, table: str) -> bool:
        """Deletes the input table in the current database

        Parameters
        ----------
        db : str
            name of the database to connect
        table : str
            name of the table to delete
        
        Returns
        -------
        bool
            True if table is deleted else False
        """
        # authenticate whether table name exists or not
        authenticate = self._auth.auth_table(db, table)
        try:
            if authenticate is True:
                self.cursor.execute(f"use {db}")
                query = f"drop table {table}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def truncate_table(self, db: str, table: str) -> bool:
        """Truncates the data of the input table

        Parameters
        ----------
        db : str
            name of the database to connect
        table : str
            name of the table to truncate
        
        Returns
        -------
        bool
            True if table is truncated else False
        """
        # authenticate whether table name exists or not
        authenticate = self._auth.auth_table(db, table)
        try:
            if authenticate is True:
                self.cursor.execute(f"use {db}")
                query = f"truncate table {table}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def desc_table(self, db: str, table: str) -> Union[str, bool]:
        """Returns the decription of structure of the input table,
        formatted using tabulate

        Parameters
        ----------
        db : str
            name of the database to connect
        table : str
            name of the table to show
        
        Returns
        -------
        str
            table description
        bool
            False if any error occurs
        """
        # authenticate whether table name exists or not
        authenticate = self._auth.auth_table(db, table)
        try:
            if authenticate is True:
                self.cursor.execute(f"use {db}")
                query = f"desc {table}"
                self.cursor.execute(query)
                desc_result = self.cursor.fetchall()

                # tabulate the table structure
                result = tabulate.tabulate(
                    desc_result,
                    headers = [
                        "Field",
                        "Type",
                        "Null",
                        "Key",
                        "Default",
                        "Extra"
                    ],
                    tablefmt = "psql"
                )
                return result

            else:
                return False

        except:
            return False

    def alter_table(self, db: str, table: str, args: List[str]) -> bool:
        """Alters the content of the input table, if
        the table exists and the column name is valid

        Parameters
        ----------
        db : str
            name of the database to connect
        table : str
            name of the table to alter
        args : list
            arguments for altering
        
        Returns
        -------
        bool
            True if table is altered else False
        """
        # authenticate whether table name exists or not
        authenticate = self._auth.auth_table(db, table)

        try:
            if authenticate is True:
                # create `Alter` class instance
                const = Alter(self.uname, self.passw, db, table)
                args[1] = args[1].lstrip(" ")

                if args[0] == "add":
                    if const.add_column(args[1]) is True:
                        return True

                    else:
                        return False

                elif args[0] == "modify":
                    if const.modify_column(args[1]) is True:
                        return True

                    else:
                        return False

                elif args[0] == "drop":
                    if const.drop_column(args[1]) is True:
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
    """Class for implementation of variations of `DDL.alter_table`
    command (add column, modify column, drop column)

    Attributes
    ----------
    username : str
        local MySQL server username
    password : str
        local MySQL server password
    database : str
        name of database to connect
    table : str
        name of table to alter
    
    Methods
    -------
    add_column
        add a new column in the table
    drop_column
        drop an existing column
    modify_column
        modify an existing column
    """

    def __init__(self, username: str, password: str, database: str, table: str):
        self.uname = username
        self.passw = password
        self.table = table
        self.db = database
        # create a `Database` class instance
        self._auth = auth.Database(self.uname, self.passw)
        self.connection = mc.connect(
            host = "localhost",
            user = self.uname,
            password = self.passw,
            database = self.db,
            autocommit = True
        )
        self.cursor = self.connection.cursor(buffered = True)

    def add_column(self, column: str) -> bool:
        """Adds the input column into the current table 
        if the column name is valid

        Parameters
        ----------
        column : str
            column arguments
        
        Returns
        -------
        bool
            True if column is added else False
        """
        try:
            query = f"alter table {self.table} add {column}"
            self.cursor.execute(query)
            return True

        except:
            return False

    def drop_column(self, column: str) -> bool:
        """Deletes the input column from the current
        table if the column name is valid

        Parameters
        ----------
        column : str
            column arguments
        
        Returns
        -------
        bool
            True if column is deleted else False
        """
        # authenticate whether column details exist in table or not
        authenticate = self._auth.auth_table_columns(self.db, self.table, column)
        try:
            if authenticate is True:
                query = f"alter table {self.table} drop column {column}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False

    def modify_column(self, column: str) -> bool:
        """Modifies the input column name along with input
        column value type if column name is valid

        Parameters
        ----------
        column : str
            column arguments
        
        Returns
        -------
        bool
            True if column is modified else False
        """
        auth_column = column.split(" ")
        # authenticate whether column details exist in table or not
        authenticate = self._auth.auth_table_columns(self.db, self.table, auth_column[0])
        try:
            if authenticate is True:
                query = f"alter table {self.table} modify column {column}"
                self.cursor.execute(query)
                return True

            else:
                return False

        except:
            return False
