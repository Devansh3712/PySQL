"""
module for menus
and ascii arts
"""

ascii_art = """

8888888b.            .d8888b.   .d88888b.  888      
888   Y88b          d88P  Y88b d88P" "Y88b 888      
888    888          Y88b.      888     888 888      
888   d88P 888  888  "Y888b.   888     888 888      
8888888P"  888  888     "Y88b. 888     888 888      
888        888  888       "888 888 Y8b 888 888      
888        Y88b 888 Y88b  d88P Y88b.Y8b88P 888      
888         "Y88888  "Y8888P"   "Y888888"  88888888 
                888                   Y8b           
           Y8b d88P                                 
            "Y88P"                                  
"""

menu = """
OPTIONS
    -a  about       Shows information about PySQL
    -c  commands    Display available commands
    -h  help        Display this help message
    -v  version     Display application version
    -q  quit        Exit the program
"""

about = """
PySQL: Python - MySQL wrapper tool

PySQL is a command line tool for making MySQL queries easier, made using Python
See https://github.com/Devansh3712/PySQL for more information
"""

commands = """
COMMANDS
    ddl    Displays Data Definition Language commands
    dml    Displays Data Manipulation Language commands
    all    Displays all SQL commands
"""

data_definition_language = """
DDL COMMANDS
    showdb                       Display all databases in MySQL server
    createdb    DB_NAME          Create a new database
    dropdb      DB_NAME          Delete a database
    showtb                       Display all tables in current db
    createtb    TB_NAME, ARGS    Create a new table in current db
    droptb      TB_NAME          Delete a table in current db
    trunctb     TB_NAME          Truncate a table in current db
    desctb      TB_NAME          Display structure of a table in current db
    altertb     TB_NAME, ARGS    Alter contents of table in current db
"""

data_manipulation_language = """
DML COMMANDS
    select  TB_NAME, COLUMNS, ARGS   Displays selected columns of current table
"""


"""
PySQL
Devansh Singh, 2021
"""
