"""
module for data-manipulation
language based commands
"""

try:
    import mysql.connector as mc
    import packages.auth as auth
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

    def __init__(self, username: str, password: str, database: str):

        self.uname = username
        self.passw = password
        self.db = database
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

    def select(self, table: str, columns: str, args: str):
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
        authenticate = self.const.auth_table(table)

        if (authenticate is True):
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

                query = ""
                if "sum" in args or "min" in args or "max" in args or "avg" in args or "count" in args:
                    query = f"select {columns} from {table} having {args}"

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


"""
PySQL
Devansh Singh, 2021
"""
