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
                            MySQL server
                            [returns boolean value]

    :drop_database:     ->  if the `database` name is valid,
                            deleting the database from server
                            [returns boolean value]

    :use_database:      ->  change the current database with a new
                            database by closing the current cursor
                            object and MySQL connection and initializing
                            new `self.connection`, `self.cursor` and
                            `self.db`
                            [returns False if database isn't authenticated]

    :create_table:      ->  takes comma separated string arguments,
                            converting them into SQL statements and
                            creating a table in the chosen database
                            [returns boolean value]

    :drop_table:        ->  if the `table` name is valid,
                            deletes the table from chosen database
                            [returns boolean value]

    :truncate_table:    ->  delete all the data in the provided table
                            without deleting the table
                            [returns boolean value]

    :desc_table:        ->  if the `table` name is valid, returns
                            the structure of the provided table,
                            formatted using tabulate
                            [returns formatted table else returns False]

    :alter_table:       ->  if the `table` name is valid, and the column
                            name is authenticated, alters the structure
                            of the input table in the current database
                            [returns boolean value]
    '''

    def __init__(self, username: str, password: str, database: str):
        
        self.uname = username
        self.passw = password
        self.db = database
        #create a `Database` class instance
        self.const = auth.Database(self.uname, self.passw, self.db)
        #authenticate data using auth module
        authenticate = self.const.authenticate()
        
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

        '''
        creates a new database in the MySQL server of the
        local machine, executing the SQL query
        `create database <db_name>`
        '''

        try:
            query = f"create database {database}"
            self.cursor.execute(query)
            return True

        except:
            return False

    def use_database(self, database: str):

        '''
        change the current database, if the input database
        exists and is valid else returns False

        it authenticates the input database, if authentication
        returns True, current MySQL connection and cursor object
        are closed, value of `self.db` is changed and a new
        MySQL connection `self.connection` & cursor object
        `self.cursor` are initialized with `self.db`
        '''

        #authenticate whether database exists or not
        authenticate = self.const.auth_db(database)
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
            return False

    def drop_database(self, database: str) -> bool:

        '''
        drops/deletes the input database in the MySQL Server,
        if it exists and is valid, executing the SQL query 
        `drop database <db_name>`
        '''

        #authenticate whether database exists or not
        authenticate = self.const.auth_db(database)
        if (authenticate == True):

            query = f"drop database {database}"
            self.cursor.execute(query)
            return True

        else:
            return False

    def create_table(self, *args) -> bool:

        '''
        creates a table in the current database with 
        provided arguments in the form of SQL statement,
        executing the SQL query `create table <table_name> (data)`
        '''

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

        '''
        drops/deletes the input table in the current
        database if table exists and is valid,
        executing the SQL query `drop table <table_name>`
        '''

        #authenticate whether table name exists or not
        authenticate = self.const.auth_table(table)
        if (authenticate == True):

            query = f"drop table {table}"
            self.cursor.execute(query)
            return True

        else:
            return False

    def truncate_table(self, table: str) -> bool:

        '''
        deletes the data of the input table, if the
        table exists and is valid, executing the
        SQL query `truncate table <table_name>`
        '''

        #authenticate whether table name exists or not
        authenticate = self.const.auth_table(table)
        if (authenticate == True):

            query = f"truncate table {table}"
            self.cursor.execute(query)
            return True

        else:
            return False

    def desc_table(self, table: str):

        '''
        returns the structure of the input table,
        formatted using `tabulate` module if the
        table exists and is valid

        representation of the SQL query `desc <table_name>`
        '''

        #authenticate whether table name exists or not
        authenticate = self.const.auth_table(table)
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

    def alter_table(self, table: str, *args) -> bool:

        '''
        alters the content of the input table, if
        the table exists and the column name is valid

        option for alter table are `add`, `modify column`
        and `drop_column`, using the `Alter` class
        '''

        #authenticate whether table name exists or not
        authenticate = self.const.auth_table(table)
        if (authenticate == True):

            #create `Alter` class instance
            const = Alter(self.uname, self.passw, self.db, table)
            
            if (args[0] == "add"):
                if (const.add_column(args[1]) == True):
                    return True
                
                else:
                    return False

            elif (args[0] == "modify"):
                if (const.modify_column(args[1]) == True):
                    return True
                
                else:
                    return False

            elif (args[0] == "drop"):
                if (const.drop_column(args[1]) == True):
                    return True
                
                else:
                    return False

            else:
                return False


class Alter:

    '''
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
    '''

    def __init__(self, username: str, password: str, database: str, table: str):

        self.uname = username
        self.passw = password
        self.db = database
        self.table = table
        #create a `Database` class instance
        self.const = auth.Database(self.uname, self.passw, self.db)

        self.connection = mc.connect(
            host = "localhost",
            user = f"{self.uname}",
            password = f"{self.passw}",
            database = f"{self.db}",
            autocommit = True
        )
        self.cursor = self.connection.cursor(buffered = True)

    def add_column(self, column: str) -> bool:

        '''
        adds the input column into the current
        table if the column name is valid, using
        the SQL query `alter table <table_name> add <column_name>`
        '''

        try:
            query = f"alter table {self.table} add {column}"
            self.cursor.execute(query)
            return True

        except:
            return False

    def drop_column(self, column: str) -> bool:

        '''
        drops/deletes the input column from the current
        table if the column name is valid, using the
        SQL query `alter table <table_name> drop column <column_name>` 
        '''

        #authenticate whether column details exist in table or not
        authenticate = self.const.auth_table_columns(self.table, column)
        if (authenticate == True):

            query = f"alter table {self.table} drop column {column}"
            self.cursor.execute(query)
            return True

        else:
            return False

    def modify_column(self, column: str) -> bool:

        '''
        modifies the input column name along with input
        column value type if column name is valid, using
        the SQL query `alter table <table_name> modify column <column_name> <value>`
        '''

        auth_column = column.split(' ')
        #authenticate whether column details exist in table or not
        authenticate = self.const.auth_table_columns(self.table, auth_column[0])
        if (authenticate == True):

            query = f"alter table {self.table} modify column {column}"
            self.cursor.execute(query)
            return True

        else:
            return False

'''
PySQL
Devansh Singh, 2021
'''