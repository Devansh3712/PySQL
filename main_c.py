"""
module for running
PySQL Python Wrapper CLI
"""

try:
    import stdiomask
    import time
    import platform
    import sys
    from colorama import init, Fore, Style
    import packages.auth as auth
    import packages.ddl_commands as ddl
    import packages.dml_commands as dml
    import data.info as info

except:
    raise Exception("Package Error: modules not setup")


__version__ = "0.0.1"
__author__ = "Devansh Singh"
__email__ = "devanshamity@gmail.com"
__license__ = "MIT"


if platform.system() == "Windows":
    init(convert = True)

print(f"{Fore.LIGHTRED_EX}{info.ascii_art}{Style.RESET_ALL}")
time.sleep(1)

sys.stdout.write(f"{Fore.CYAN}Username: {Style.RESET_ALL}")
uname = input()
passwd = stdiomask.getpass(prompt = f"{Fore.CYAN}Password: {Style.RESET_ALL}")
sys.stdout.write(f"{Fore.CYAN}Database: {Style.RESET_ALL}")
dbname = input()

authenticate = auth.Database(uname, passwd, dbname).authenticate()
if authenticate is False:
    print(f"{Fore.RED}[-]Credentials could not be authenticated{Style.RESET_ALL}")
    exit()

print(f"{Fore.GREEN}[+]Connected to database {Style.RESET_ALL}{dbname}")
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
            print(f"{Fore.RED}[-]Unable to show databases{Style.RESET_ALL}\n")

    elif user_input.lower() == "createdb":
        db_name = input("pysql> Enter database name: ")
        result = ddl_obj.create_database(db_name)

        if result is True:
            print(f"{Fore.GREEN}[+]Created database {Style.RESET_ALL}{db_name}\n")

        else:
            print(f"{Fore.RED}[-]Unable to create database {Style.RESET_ALL}{db_name}\n")

    elif user_input.lower() == "dropdb":
        db_name = input("pysql> Enter database name: ")

        if db_name != dbname:
            result = ddl_obj.drop_database(db_name)

            if result is True:
                print(f"{Fore.GREEN}[+]Deleted database {Style.RESET_ALL}{db_name}\n")

            else:
                print(f"{Fore.RED}[-]Unable to delete database {Style.RESET_ALL}{db_name}\n")

        else:
            print(f"{Fore.RED}[-]Cannot delete database in use{Style.RESET_ALL}\n")

    elif user_input.lower() == "showtb":
        result = ddl_obj.show_tables()

        if result:
            print(result + "\n")

        else:
            print("{Fore.RED}[-]Unable to show tables{Style.RESET_ALL}\n")

    elif user_input.lower() == "createtb":
        tb_name = input("pysql> Enter table name: ")
        args = input("pysql> Enter table details: ")
        args = args.split(",")
        result = ddl_obj.create_table(tb_name, args)

        if result is True:
            print(f"{Fore.GREEN}[+]Created table {Style.RESET_ALL}{tb_name}\n")

        else:
            print(f"{Fore.RED}[-]Unable to create table {Style.RESET_ALL}{tb_name}\n")

    elif user_input.lower() == "droptb":
        tb_name = input("pysql> Enter table name: ")
        result = ddl_obj.drop_table(tb_name)

        if result is True:
            print(f"{Fore.GREEN}[+]Deleted table {Style.RESET_ALL}{tb_name}\n")

        else:
            print(f"{Fore.RED}[-]Unable to delete table {Style.RESET_ALL}{tb_name}\n")

    elif user_input.lower() == "trunctb":
        tb_name = input("pysql> Enter table name: ")
        result = ddl_obj.truncate_table(tb_name)

        if result is True:
            print(f"{Fore.GREEN}[+]Truncated table {Style.RESET_ALL}{tb_name}\n")

        else:
            print(f"{Fore.RED}[-]Unable to truncate table {Style.RESET_ALL}{tb_name}\n")

    elif user_input.lower() == "desctb":
        tb_name = input("pysql> Enter table name: ")
        result = ddl_obj.desc_table(tb_name)

        if result:
            print(result + "\n")

        else:
            print(f"{Fore.RED}[-]Unable to display table {Style.RESET_ALL}{tb_name}\n")

    elif user_input.lower() == "altertb":
        tb_name = input("pysql> Enter table name: ")
        args = input("pysql> Enter arguments: ")
        args = args.split(",")
        result = ddl_obj.alter_table(tb_name, args)

        if result is True:
            print(f"{Fore.GREEN}[+]Altered table {Style.RESET_ALL}{tb_name}\n")

        else:
            print(f"{Fore.RED}[-]Unable to alter table {Style.RESET_ALL}{tb_name}\n")

    elif user_input.lower() == "dml":
        print(info.data_manipulation_language)

    else:
        print("Choose a valid option")


"""
PySQL
Devansh Singh, 2021
"""
