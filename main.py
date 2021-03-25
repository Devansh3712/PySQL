"""
module for running
PySQL Python Wrapper CLI
"""

try:
    import stdiomask
    import time
    import packages.ddl_commands as ddl
    import packages.dml_commands as dml
    import data.info as info

except:
    raise Exception("Package Error: modules not setup")


__version__ = "0.0.1"
__author__ = "Devansh Singh"
__email__ = "devanshamity@gmail.com"
__license__ = "MIT"


print(info.ascii_art)
time.sleep(1)

uname = input("Username: ")
passwd = stdiomask.getpass(prompt = "Password: ")
dbname = input("Database: ")
user = ddl.DDL(uname, passwd, dbname)

print(f"[+]Connected to database {dbname}")
time.sleep(1)

print(info.menu)

while (True):

    user_input = input("pysql> ")
    ddl_obj = ddl.DDL(uname, passwd, dbname)

    if user_input.lower() in ["-a", "about"]:
        print(info.about)

    elif user_input.lower() in ["-h", "help"]:
        print(info.menu)

    elif user_input.lower() in ["-q", "quit"]:
        exit()

    elif user_input.lower() in ["-c", "commands"]:
        print(info.commands)

    elif user_input.lower() in ["-v", "version"]:
        print(__version__)

    elif user_input.lower() == "ddl":
        print(info.data_definition_language)

    elif user_input.lower() == "showdb":
        result = ddl_obj.show_databases()

        if result:
            print(result + "\n")
        
        else:
            print("[-]Unable to show databases\n")

    elif user_input.lower() == "createdb":
        db_name = input("pysql> Enter database name: ")
        result = ddl_obj.create_database(db_name)

        if result is True:
            print(f"[+]Created database {db_name}\n")

        else:
            print(f"[-]Unable to create database {db_name}\n")

    elif user_input.lower() == "usedb":
        db_name = input("pysql> Enter database name: ")
        result = ddl_obj.use_database(db_name)

        if result is True:
            print(f"[+]Connected to database {db_name}\n")

        else:
            print(f"[-]Unable to use database {db_name}\n")

    elif user_input.lower() == "dropdb":
        db_name = input("pysql> Enter database name: ")
        result = ddl_obj.drop_database(db_name)

        if result is True:
            print(f"[+]Deleted database {db_name}\n")

        else:
            print(f"[-]Unable to delete database {db_name}\n")

    elif user_input.lower() == "showtb":
        result = ddl_obj.show_tables()

        if result:
            print(result + "\n")

        else:
            print("[-]Unable to show tables\n")

    elif user_input.lower() == "createtb":
        tb_name = input("pysql> Enter table details: ")
        tb_name = tb_name.split(",")
        result = ddl_obj.create_table(tb_name)

        if result is True:
            print(f"[+]Created table {tb_name[0]}\n")

        else:
            print(f"[-]Unable to create table {tb_name[0]}\n")

    elif user_input.lower() == "droptb":
        tb_name = input("pysql> Enter table name: ")
        result = ddl_obj.drop_table(tb_name)

        if result is True:
            print(f"[+]Deleted table {tb_name}\n")

        else:
            print(f"[-]Unable to delete table {tb_name}\n")

    elif user_input.lower() == "trunctb":
        tb_name = input("pysql> Enter table name: ")
        result = ddl_obj.truncate_table(tb_name)

        if result is True:
            print(f"[+]Truncated table {tb_name}\n")

        else:
            print(f"[-]Unable to truncate table {tb_name}\n")

    elif user_input.lower() == "desctb":
        tb_name = input("pysql> Enter table name: ")
        result = ddl_obj.desc_table(tb_name)

        if result:
            print(result + "\n")

        else:
            print(f"[-]Unable to display table {tb_name}\n")

    elif user_input.lower() == "altertb":
        tb_name = input("pysql> Enter table name: ")
        args = input("pysql> Enter arguments: ")
        args = args.split(",")
        result = ddl_obj.alter_table(tb_name, args)

        if result is True:
            print(f"[+]Altered table {tb_name}\n")

        else:
            print(f"[-]Unable to alter table {tb_name}\n")

    elif user_input.lower() == "dml":
        print(data_manipulation_language)

    else:
        print("Choose a valid option")


"""
PySQL
Devansh Singh, 2021
"""
