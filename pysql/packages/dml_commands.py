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

    :select:        ->  if the `table` name is valid, shows
                        the table with value of selected columns
                        with given arguments, formatted with tabulate
                        [returns formatted table else False]

    :insert_single: ->  if the `table` name is valid, inserts the
                        input value (single row) into the
                        table
                        [returns boolean value]
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

        try:
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

    def insert_single(self, table: str, args: str):
        """
        inserts a single row into the selected
        table, executing the SQL query
        `insert into <tb_name> values (<args>)`

        args    ->  comma separated values to
                    to be entered in the table
        """
        # authenticate whether the table exists or not
        authenticate = self.const.auth_table(table)

        try:
            if (authenticate is True):

                # create list of values to be inserted
                args = args.split(",")
                self.cursor.execute(f"select * from {table}")
                # get column names
                columns = self.cursor.column_names

                # number of columns and number of values inserted should be equal
                if len(args) != len(columns):
                    return False

                else:

                    # get table description
                    table_desc = self.cursor.description
                    # filter out column types
                    table_desc = [mc.FieldType.get_info(table_desc[i][1]) for i in range (len(table_desc))]
                    args = [x.strip(" ") for x in args]

                    # designate proper datatypes to values
                    for v, t in zip(args, table_desc):

                        if t in ["DECIMAL", "FLOAT"]:
                            v = float(v)

                        elif t in ["TINY", "SHORT", "LONG", "LONGLONG", "INT", "INT24", "TINYINT"]:
                            v = int(v)

                    query = f"insert into {table} values {tuple(args)}"
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
