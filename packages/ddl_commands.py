'''
module for data-definition
language based commands
'''

try:
    import mysql.connector as mc
    import tabulate
    import auth

except:
    raise Exception("'ddl_commands' modules not setup")

class DDL:

    '''
    class for implementation of Data Definition Language
    based commands (create, drop, alter)

    :create_database:   ->  create a new database in the
                            MySQL server by executing the
                            SQL query `create database <db_name>`

    :drop_database:     ->  if the `database` name is valid,
                            executes the SQL query `drop database <db_name>`
                            deleting the database from server

    :use_database:      ->  change the current database with a new
                            database by closing the current cursor
                            object and MySQL connection and initializing
                            new `self.connection`, `self.cursor` and
                            `self.db`

    :create_table:      ->  takes comma separated string arguments
                            and executes the SQL query `create table <table_name>`
                            creating a table in the chosen database

    :drop_table:        ->  if the `table` name is valid, executes
                            the SQL query `drop table <table_name>` 
                            deleting the table from chosen database

    :desc_table:        ->  if the `table` name is valid, executes
                            the SQL query `desc <table_name>` returning
                            the structure of the provided table,
                            formatted using tabulate
    '''

    def __init__(self, username: str, password: str, database: str):
        
        self.uname = username
        self.passw = password
        self.db = database
        #authenticate data using auth module
        authenticate = auth.Database(self.uname, self.passw, self.db).authenticate()
        
        if (authenticate == True):
            #initialize connection with MySQL server and cursor object for execution of commands
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

    def create_database(self, database: str) -> bool:

        try:
            query = f"create database {database}"
            self.cursor.execute(query)
            return True

        except:
            return False

    def use_database(self, database: str):

        #authenticate whether database exists or not
        authenticate = auth.Database(self.uname, self.passw, self.db).auth_db(database)
        if (authenticate == True):

            #close the current cursor object and MySQL connection
            self.cursor.close()
            self.connection.close()
            #change the value of `self.db`
            self.db = database

            #create new connection with MySQL server and cursor object
            self.connection = mc.connect(
                host = "localhost",
                user = f"{self.uname}",
                password = f"{self.passw}",
                database = f"{self.db}",
                autocommit = True
            )
            self.cursor = self.connection.cursor(buffered = True)

        else:
            raise Exception("Unable to change database")

    def drop_database(self, database: str) -> bool:

        #authenticate whether database exists or not
        authenticate = auth.Database(self.uname, self.passw, self.db).auth_db(database)
        if (authenticate == True):

            query = f"drop database {database}"
            self.cursor.execute(query)
            return True

        else:
            return False

    def create_table(self, *args) -> bool:

        try:
            #statement with column parameters for MySQL table
            statement = '('
            for num in range (1, len(args)):

                if (num == len(args) - 1):
                    statement += args[num] + ')'
                
                else:
                    statement += args[num] + ', '

            query = f"create table {args[0]} {statement}"
            self.cursor.execute(query)
            return True

        except:
            return False

    def drop_table(self, table: str) -> bool:

        #authenticate whether table name exists or not
        authenticate = auth.Database(self.uname, self.passw, self.db).auth_table(table)
        if (authenticate == True):

            query = f"drop table {table}"
            self.cursor.execute(query)
            return True

        else:
            return False

    def desc_table(self, table: str):

        #authenticate whether table name exists or not
        authenticate = auth.Database(self.uname, self.passw, self.db).auth_table(table)
        if (authenticate == True):

            query = f"desc {table}"
            self.cursor.execute(query)
            desc_result = self.cursor.fetchall()

            #tabulate the table structure
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

    def alter_table(self, table: str, query: str) -> bool:

        #authenticate whether table name exists or not
        authenticate = auth.Database(self.uname, self.passw, self.db).auth_table(table)
        if (authenticate == True):

            auth_column = auth.Database(self.uname, self.passw, self.db).auth_table_columns(table)

'''
PySQL
Devansh Singh, 2021
'''