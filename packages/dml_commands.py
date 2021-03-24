"""
module for data-manipulation
language based commands
"""

try:
    import mysql.connector as mc
    import auth
    import tabulate

except:
    raise Exception("'dml_commands' module not setup")


class DML:
    """
    class for implementation of Data Manipulation Language
    based commands (select, update, delete, insert)

    :select:    ->  if the `table` name is valid, shows
                    the table with value of selected columns
                    with given arguments, formatted with tabulate
                    [returns formatted table else False]
    """

    def __init__(self, username: str, password: str, database: str, table: str):

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

    def select(self, columns: str = "*", args: str = None):
        """
        Shows the selected components of the current
        table, executing the SQL query
        `select <columns> from <table_name> where <args>`

        columns ->  columns to be chosen, default is `*` 
                    (all columns)
        args    ->  arguments for the select query, default
                    is `None`
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_table(self.table)

        if (authenticate is True):
            # if no arguments are provided for selection
            if (args is None):

                query = f"select {columns} from {self.table}"
                self.cursor.execute(query)
                select_result = self.cursor.fetchall()
                # provides column names in the input table
                table_columns = self.cursor.column_names

                result = tabulate.tabulate(
                    select_result,
                    headers = [data for data in table_columns],
                    tablefmt = "psql"
                )
                return result

            else:

                query = f"select {columns} from {self.table} where {args}"
                self.cursor.execute(query)
                select_result = self.cursor.fetchall()
                # provides column names in the input table
                table_columns = self.cursor.column_names

                result = tabulate.tabulate(
                    select_result,
                    headers = [data for data in table_columns],
                    tablefmt = "psql"
                )
                return result

        else:
            return False


"""
PySQL
Devansh Singh, 2021
"""
