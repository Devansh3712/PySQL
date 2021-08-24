"""
module for running
PySQL Python Wrapper CLI
[colored version]
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

try:
    import pysql.utils.exceptions as exceptions
    import stdiomask
    import time
    import platform
    import urllib.request
    from colorama import init, Fore, Style
    import pysql.packages.auth as auth
    import pysql.packages.ddl_commands as ddl
    import pysql.packages.dml_commands as dml
    import pysql.data.info as info
    import pysql.data.export as export
    import pysql.data.imports as imports
    import pysql.utils.update as update
    import pysql.utils.user as user

except:
    raise exceptions.PySQLPackageError()

__version__ = "1.1.0"

if platform.system() == "Windows":
    init(convert = True)

print(f"{Fore.LIGHTRED_EX}{info.ascii_art}{Style.RESET_ALL}")
time.sleep(1)

# check if a default user exists
check = user.User().check_default_user()

if check is True:
    # get default user's name
    def_user = user.User().get_default_user()
    print(f"\n[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Default user {Style.RESET_ALL}{Fore.CYAN}{def_user[0]}{Style.RESET_ALL}{Fore.GREEN} authenticated{Style.RESET_ALL}")
    uname = def_user[0]
    passwd = def_user[1]

else:
    sys.stdout.write(f"{Fore.CYAN}Username: {Style.RESET_ALL}")
    uname = input()
    passwd = stdiomask.getpass(prompt = f"{Fore.CYAN}Password: {Style.RESET_ALL}")

    authenticate = auth.Database(uname, passwd).authenticate()
    if authenticate is False:
        print(f"\n[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} User could not be authenticated{Style.RESET_ALL}")
        exit()

    print(f"\n[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} User authenticated{Style.RESET_ALL}")

time.sleep(1)
print(info.menu)

# package class instances as objects for calling functions
ddl_obj = ddl.DDL(uname, passwd)
dml_obj = dml.DML(uname, passwd)
exp_obj = export.Export(uname, passwd)
imp_obj = imports.Import(uname, passwd)

# information of database in use
current_db = ""
db_use = False

while (True):

    if db_use is True:
        sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> ")
        user_input = input()

    else:
        user_input = input("pysql> ")

    try:

        if user_input.lower() in ["-a", "about"]:
            print(info.about)

        elif user_input.lower() in ["-h", "help"]:
            print(info.menu)

        elif user_input.lower() in ["-q", "quit"]:
            print(f"{Fore.LIGHTMAGENTA_EX}Goodbye{Style.RESET_ALL}")
            break

        elif user_input.lower() in ["-c", "commands"]:
            print(info.commands)

        elif user_input.lower() in ["-v", "version"]:
            print(__version__ + "\n")

        elif user_input.lower() in ["-d", "def user"]:
            print(info.default_user)

        elif user_input.lower() in ["-u", "updates"]:
            gh_version = urllib.request.urlopen("https://raw.githubusercontent.com/Devansh3712/PySQL/main/pysql/__version__.py")
            gh_version = gh_version.read().decode("utf-8")

            if gh_version > __version__:

                result = update.update_pysql()

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} PySQL updated to v{gh_version} succesfully{Style.RESET_ALL}\n")
                    break

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to update PySQL{Style.RESET_ALL}\n")

            else:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} PySQL is up-to-date{Style.RESET_ALL}\n")

        elif user_input.lower() == "adduser":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter username: ")
                _uname = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter password: ")
                _passwd = stdiomask.getpass(prompt = "")

            else:
                _uname = input("pysql> Enter username: ")
                _passwd = stdiomask.getpass(prompt = "pysql> Enter password: ")

            result = user.User().add_default_user(_uname, _passwd)

            if result is True:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Default user {Style.RESET_ALL}{Fore.CYAN}{_uname}{Style.RESET_ALL}{Fore.GREEN} created{Style.RESET_ALL}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to create default user{Style.RESET_ALL}\n")

        elif user_input.lower() == "removeuser":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter password: ")
                _passwd = stdiomask.getpass(prompt = "")

            else:
                _passwd = stdiomask.getpass(prompt = "pysql> Enter password: ")

            def_user = user.User().get_default_user()
            if _passwd == def_user[1]:
                result = user.User().remove_default_user()

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Default user {Style.RESET_ALL}{Fore.CYAN}{def_user[0]}{Style.RESET_ALL}{Fore.GREEN} removed{Style.RESET_ALL}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to remove default user{Style.RESET_ALL}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to authenticate{Style.RESET_ALL}\n")

        elif user_input.lower() == "ddl":
            print(info.data_definition_language)

        elif user_input.lower() == "showdb":
            result = ddl_obj.show_databases()

            if result:
                print(result + "\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to show databases{Style.RESET_ALL}\n")

        elif user_input.lower() == "createdb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter database name: ")
                db_name = input()

            else:
                db_name = input("pysql> Enter database name: ")

            result = ddl_obj.create_database(db_name)

            if result is True:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Created database {Style.RESET_ALL}{db_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to create database {Style.RESET_ALL}{db_name}\n")

        elif user_input.lower() == "usedb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter database name: ")
                db_name = input()

            else:
                db_name = input("pysql> Enter database name: ")

            result = ddl_obj.use_database(db_name)

            if result is True:
                current_db = db_name
                db_use = True
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Connected to database {Style.RESET_ALL}{db_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to connect to database {Style.RESET_ALL}{db_name}\n")

        elif user_input.lower() == "dropdb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter database name: ")
                db_name = input()

            else:
                db_name = input("pysql> Enter database name: ")

            result = ddl_obj.drop_database(db_name)

            if result is True:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Deleted database {Style.RESET_ALL}{db_name}\n")
                current_db = ""
                db_use = False

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to delete database {Style.RESET_ALL}{db_name}\n")

        elif user_input.lower() == "showtb":

            if db_use is True:
                result = ddl_obj.show_tables()

                if result:
                    print(result + "\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to show tables{Style.RESET_ALL}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "createtb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table details: ")
                args = input()
                args = args.split(",")
                result = ddl_obj.create_table(current_db, tb_name, args)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Created table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to create table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "droptb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                result = ddl_obj.drop_table(current_db, tb_name)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Deleted table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to delete table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "trunctb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                result = ddl_obj.truncate_table(current_db, tb_name)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Truncated table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to truncate table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "desctb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                result = ddl_obj.desc_table(current_db, tb_name)

                if result:
                    print(result + "\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to display table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "altertb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter arguments: ")
                args = input()
                args = args.split(",")
                result = ddl_obj.alter_table(current_db, tb_name, args)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Altered table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to alter table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "dml":
            print(info.data_manipulation_language)

        elif user_input.lower() == "select":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter selection columns: ")
                columns = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table details: ")
                args = input()
                result = dml_obj.select(current_db, tb_name, columns, args)

                if result:
                    print(result + "\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to show selected values{Style.RESET_ALL}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() in ["insert -s", "insert"]:

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter values: ")
                args = input()
                result = dml_obj.insert(current_db, tb_name, args)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Inserted values in table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to insert value in table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "insert -m":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter number of records: ")
                num = int(input())
                flag = True

                for records in range (num):
                    sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter values: ")
                    args = input()
                    result = dml_obj.insert(current_db, tb_name, args)

                    if result is False:
                        print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to insert value in table {Style.RESET_ALL}{tb_name}\n")
                        flag = False
                        break

                if flag is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Inserted values in table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "insert -f":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter path to CSV file: ")
                path = input()
                result = dml_obj.insert_file(current_db, tb_name, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Inserted values in table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to insert value in table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "update":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter columns to update: ")
                columns = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter arguments: ")
                args = input()
                result = dml_obj.update(current_db, tb_name, columns, args)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Updated values in table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to update values in table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "delete":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter columns to delete: ")
                columns = input()
                result = dml_obj.delete(current_db, tb_name, columns)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Deleted values from table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to delete values from table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "all":
            print(info.all_commands)

        elif user_input.lower() == "export":
            print(info.export)

        elif user_input.lower() == "import":
            print(info.import_)

        elif user_input.lower() == "exportdb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter database name: ")
                db_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter path to export: ")
                path = input()

            else:
                db_name = input("pysql> Enter database name: ")
                path = input("pysql> Enter path to export: ")

            result = exp_obj.export_database(db_name, path)

            if result is True:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported database {Style.RESET_ALL}{db_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export database {Style.RESET_ALL}{db_name}\n")

        elif user_input.lower() == "exporttb -json":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter path to export: ")
                path = input()
                result = exp_obj.export_table_json(current_db, tb_name, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "exporttb -csv":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter path to export: ")
                path = input()
                result = exp_obj.export_table_csv(current_db, tb_name, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "exporttb -sql":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter path to export: ")
                path = input()
                result = exp_obj.export_table_sql(current_db, tb_name, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "exportall -json":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter path to export: ")
                path = input()
                result = exp_obj.export_all_json(current_db, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported all tables in {Style.RESET_ALL}{current_db}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export tables in {Style.RESET_ALL}{current_db}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "exportall -csv":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter path to export: ")
                path = input()
                result = exp_obj.export_all_csv(current_db, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported all tables in {Style.RESET_ALL}{current_db}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export tables in {Style.RESET_ALL}{current_db}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "exportall -sql":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter path to export: ")
                path = input()
                result = exp_obj.export_all_sql(current_db, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported all tables in {Style.RESET_ALL}{current_db}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export tables in {Style.RESET_ALL}{current_db}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "importdb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter database name: ")
                db_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter path of file: ")
                path = input()

            else:
                db_name = input("pysql> Enter database name: ")
                path = input("pysql> Enter path of file: ")

            result = imp_obj.import_database(db_name, path)

            if result is True:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Imported to database {Style.RESET_ALL}{db_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to import to database {Style.RESET_ALL}{db_name}\n")

        elif user_input.lower() == "importtb":

            if db_use is True:
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter table name: ")
                tb_name = input()
                sys.stdout.write(f"{Fore.LIGHTYELLOW_EX}({current_db}){Style.RESET_ALL} pysql> Enter path of file: ")
                path = input()

            else:
                tb_name = input("pysql> Enter table name: ")
                path = input("pysql> Enter path of file: ")

            result = imp_obj.import_table(tb_name, path)

            if result is True:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Imported table to database {Style.RESET_ALL}{db_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to import table to database {Style.RESET_ALL}{db_name}\n")

        else:
            print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Choose a valid option{Style.RESET_ALL}\n")

    except:
        print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to execute command{Style.RESET_ALL}\n")

# entry point for running PySQL CLI
def cli():
    pass


"""
PySQL
Devansh Singh, 2021
"""
