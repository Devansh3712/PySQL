import os
import sys

# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

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

__version__ = "1.1.2"

if platform.system() == "Windows":
    init(convert=True)

print(f"{Fore.LIGHTRED_EX}{info.ascii_art}{reset}")
time.sleep(1)

# check if a default user exists
check = user.User().check_default_user()
# colors
green = Fore.GREEN
red = Fore.RED
cyan = Fore.CYAN
yellow = Fore.LIGHTYELLOW_EX
magenta = Fore.LIGHTMAGENTA_EX
reset = Style.RESET_ALL

if check is True:
    # get default user's name
    def_user = user.User().get_default_user()
    print(
        f"\n[{green}+{reset}]{green} Default user {reset}{cyan}{def_user[0]}{reset}{green} authenticated{reset}"
    )
    uname = def_user[0]
    passwd = def_user[1]

else:
    sys.stdout.write(f"{cyan}Username: {reset}")
    uname = input()
    passwd = stdiomask.getpass(prompt=f"{cyan}Password: {reset}")
    # authenticate user credentials
    authenticate = auth.Database(uname, passwd).authenticate()
    if authenticate is False:
        print(f"\n[{red}-{reset}]{red} User could not be authenticated{reset}")
        exit()
    print(f"\n[{green}+{reset}]{green} User authenticated{reset}")

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

while True:
    if db_use is True:
        sys.stdout.write(f"{yellow}({current_db}){reset} pysql> ")
        user_input = input()

    else:
        user_input = input("pysql> ")

    try:
        if user_input.lower() in ["-a", "about"]:
            print(info.about)

        elif user_input.lower() in ["-h", "help"]:
            print(info.menu)

        elif user_input.lower() in ["-q", "quit", "exit"]:
            print(f"{magenta}Goodbye{reset}")
            break

        elif user_input.lower() in ["-c", "commands"]:
            print(info.commands)

        elif user_input.lower() in ["-v", "version"]:
            print(__version__ + "\n")

        elif user_input.lower() in ["-d", "def user"]:
            print(info.default_user)

        elif user_input.lower() in ["-u", "updates"]:
            gh_version = urllib.request.urlopen(
                "https://raw.githubusercontent.com/Devansh3712/PySQL/main/pysql/__version__.py"
            )
            gh_version = gh_version.read().decode("utf-8")

            if gh_version > __version__:
                result = update.update_pysql()

                if result is True:
                    print(
                        f"[{green}+{reset}]{green} PySQL updated to v{gh_version} succesfully{reset}\n"
                    )
                    break

                else:
                    print(f"[{red}-{reset}]{red} Unable to update PySQL{reset}\n")

            else:
                print(f"[{green}+{reset}]{green} PySQL is up-to-date{reset}\n")

        elif user_input.lower() == "adduser":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter username: "
                )
                _uname = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter password: "
                )
                _passwd = stdiomask.getpass(prompt="")

            else:
                _uname = input("pysql> Enter username: ")
                _passwd = stdiomask.getpass(prompt="pysql> Enter password: ")

            result = user.User().add_default_user(_uname, _passwd)

            if result is True:
                print(
                    f"[{green}+{reset}]{green} Default user {reset}{cyan}{_uname}{reset}{green} created{reset}\n"
                )

            else:
                print(f"[{red}-{reset}]{red} Unable to create default user{reset}\n")

        elif user_input.lower() == "removeuser":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter password: "
                )
                _passwd = stdiomask.getpass(prompt="")

            else:
                _passwd = stdiomask.getpass(prompt="pysql> Enter password: ")

            def_user = user.User().get_default_user()

            if _passwd == def_user[1]:
                result = user.User().remove_default_user()

                if result is True:
                    print(
                        f"[{green}+{reset}]{green} Default user {reset}{cyan}{def_user[0]}{reset}{green} removed{reset}\n"
                    )

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to remove default user{reset}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} Unable to authenticate{reset}\n")

        elif user_input.lower() == "ddl":
            print(info.data_definition_language)

        elif user_input.lower() == "showdb":
            result = ddl_obj.show_databases()

            if result:
                print(result + "\n")

            else:
                print(f"[{red}-{reset}]{red} Unable to show databases{reset}\n")

        elif user_input.lower() == "createdb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter database name: "
                )
                db_name = input()

            else:
                db_name = input("pysql> Enter database name: ")

            result = ddl_obj.create_database(db_name)

            if result is True:
                print(f"[{green}+{reset}]{green} Created database {reset}{db_name}\n")

            else:
                print(
                    f"[{red}-{reset}]{red} Unable to create database {reset}{db_name}\n"
                )

        elif user_input.lower() == "usedb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter database name: "
                )
                db_name = input()

            else:
                db_name = input("pysql> Enter database name: ")

            result = ddl_obj.use_database(db_name)

            if result is True:
                current_db = db_name
                db_use = True
                print(
                    f"[{green}+{reset}]{green} Connected to database {reset}{db_name}\n"
                )

            else:
                print(
                    f"[{red}-{reset}]{red} Unable to connect to database {reset}{db_name}\n"
                )

        elif user_input.lower() == "dropdb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter database name: "
                )
                db_name = input()

            else:
                db_name = input("pysql> Enter database name: ")

            result = ddl_obj.drop_database(db_name)

            if result is True:
                print(f"[{green}+{reset}]{green} Deleted database {reset}{db_name}\n")
                current_db = ""
                db_use = False

            else:
                print(
                    f"[{red}-{reset}]{red} Unable to delete database {reset}{db_name}\n"
                )

        elif user_input.lower() == "showtb":
            if db_use is True:
                result = ddl_obj.show_tables(current_db)

                if result:
                    print(result + "\n")

                else:
                    print(f"[{red}-{reset}]{red} Unable to show tables{reset}\n")

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "createtb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table details: "
                )
                args = input()
                args = args.split(",")
                result = ddl_obj.create_table(current_db, tb_name, args)

                if result is True:
                    print(f"[{green}+{reset}]{green} Created table {reset}{tb_name}\n")

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to create table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "droptb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                result = ddl_obj.drop_table(current_db, tb_name)

                if result is True:
                    print(f"[{green}+{reset}]{green} Deleted table {reset}{tb_name}\n")

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to delete table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "trunctb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                result = ddl_obj.truncate_table(current_db, tb_name)

                if result is True:
                    print(
                        f"[{green}+{reset}]{green} Truncated table {reset}{tb_name}\n"
                    )

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to truncate table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "desctb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                result = ddl_obj.desc_table(current_db, tb_name)

                if result:
                    print(result + "\n")

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to display table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "altertb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter arguments: "
                )
                args = input()
                args = args.split(",")
                result = ddl_obj.alter_table(current_db, tb_name, args)

                if result is True:
                    print(f"[{green}+{reset}]{green} Altered table {reset}{tb_name}\n")

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to alter table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "dml":
            print(info.data_manipulation_language)

        elif user_input.lower() == "select":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter selection columns: "
                )
                columns = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table details: "
                )
                args = input()
                result = dml_obj.select(current_db, tb_name, columns, args)

                if result:
                    print(result + "\n")

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to show selected values{reset}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() in ["insert -s", "insert"]:
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(f"{yellow}({current_db}){reset} pysql> Enter values: ")
                args = input()
                result = dml_obj.insert(current_db, tb_name, args)

                if result is True:
                    print(
                        f"[{green}+{reset}]{green} Inserted values in table {reset}{tb_name}\n"
                    )

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to insert value in table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "insert -m":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter number of records: "
                )
                num = int(input())
                flag = True

                for records in range(num):
                    sys.stdout.write(
                        f"{yellow}({current_db}){reset} pysql> Enter values: "
                    )
                    args = input()
                    result = dml_obj.insert(current_db, tb_name, args)

                    if result is False:
                        print(
                            f"[{red}-{reset}]{red} Unable to insert value in table {reset}{tb_name}\n"
                        )
                        flag = False
                        break

                if flag is True:
                    print(
                        f"[{green}+{reset}]{green} Inserted values in table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "insert -f":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter path to CSV file: "
                )
                path = input()
                result = dml_obj.insert_file(current_db, tb_name, path)

                if result is True:
                    print(
                        f"[{green}+{reset}]{green} Inserted values in table {reset}{tb_name}\n"
                    )

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to insert value in table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "update":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter columns to update: "
                )
                columns = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter arguments: "
                )
                args = input()
                result = dml_obj.update(current_db, tb_name, columns, args)

                if result is True:
                    print(
                        f"[{green}+{reset}]{green} Updated values in table {reset}{tb_name}\n"
                    )

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to update values in table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "delete":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter columns to delete: "
                )
                columns = input()
                result = dml_obj.delete(current_db, tb_name, columns)

                if result is True:
                    print(
                        f"[{green}+{reset}]{green} Deleted values from table {reset}{tb_name}\n"
                    )

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to delete values from table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "all":
            print(info.all_commands)

        elif user_input.lower() == "export":
            print(info.export)

        elif user_input.lower() == "import":
            print(info.import_)

        elif user_input.lower() == "exportdb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter database name: "
                )
                db_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter path to export: "
                )
                path = input()

            else:
                db_name = input("pysql> Enter database name: ")
                path = input("pysql> Enter path to export: ")

            result = exp_obj.export_database(db_name, path)

            if result is True:
                print(f"[{green}+{reset}]{green} Exported database {reset}{db_name}\n")

            else:
                print(
                    f"[{red}-{reset}]{red} Unable to export database {reset}{db_name}\n"
                )

        elif user_input.lower() == "exporttb -json":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter path to export: "
                )
                path = input()
                result = exp_obj.export_table_json(current_db, tb_name, path)

                if result is True:
                    print(f"[{green}+{reset}]{green} Exported table {reset}{tb_name}\n")

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to export table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "exporttb -csv":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter path to export: "
                )
                path = input()
                result = exp_obj.export_table_csv(current_db, tb_name, path)

                if result is True:
                    print(f"[{green}+{reset}]{green} Exported table {reset}{tb_name}\n")

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to export table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "exporttb -sql":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter path to export: "
                )
                path = input()
                result = exp_obj.export_table_sql(current_db, tb_name, path)

                if result is True:
                    print(f"[{green}+{reset}]{green} Exported table {reset}{tb_name}\n")

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to export table {reset}{tb_name}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "exportall -json":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter path to export: "
                )
                path = input()
                result = exp_obj.export_all_json(current_db, path)

                if result is True:
                    print(
                        f"[{green}+{reset}]{green} Exported all tables in {reset}{current_db}\n"
                    )

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to export tables in {reset}{current_db}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "exportall -csv":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter path to export: "
                )
                path = input()
                result = exp_obj.export_all_csv(current_db, path)

                if result is True:
                    print(
                        f"[{green}+{reset}]{green} Exported all tables in {reset}{current_db}\n"
                    )

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to export tables in {reset}{current_db}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "exportall -sql":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter path to export: "
                )
                path = input()
                result = exp_obj.export_all_sql(current_db, path)

                if result is True:
                    print(
                        f"[{green}+{reset}]{green} Exported all tables in {reset}{current_db}\n"
                    )

                else:
                    print(
                        f"[{red}-{reset}]{red} Unable to export tables in {reset}{current_db}\n"
                    )

            else:
                print(f"[{red}-{reset}]{red} No database in use{reset}\n")

        elif user_input.lower() == "importdb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter database name: "
                )
                db_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter path of file: "
                )
                path = input()

            else:
                db_name = input("pysql> Enter database name: ")
                path = input("pysql> Enter path of file: ")

            result = imp_obj.import_database(db_name, path)

            if result is True:
                print(
                    f"[{green}+{reset}]{green} Imported to database {reset}{db_name}\n"
                )

            else:
                print(
                    f"[{red}-{reset}]{red} Unable to import to database {reset}{db_name}\n"
                )

        elif user_input.lower() == "importtb":
            if db_use is True:
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter table name: "
                )
                tb_name = input()
                sys.stdout.write(
                    f"{yellow}({current_db}){reset} pysql> Enter path of file: "
                )
                path = input()

            else:
                tb_name = input("pysql> Enter table name: ")
                path = input("pysql> Enter path of file: ")

            result = imp_obj.import_table(tb_name, path)

            if result is True:
                print(
                    f"[{green}+{reset}]{green} Imported table to database {reset}{db_name}\n"
                )

            else:
                print(
                    f"[{red}-{reset}]{red} Unable to import table to database {reset}{db_name}\n"
                )

        else:
            print(f"[{red}-{reset}]{red} Choose a valid option{reset}\n")

    except:
        print(f"[{red}-{reset}]{red} Unable to execute command{reset}\n")

# entry point for running PySQL CLI
def cli():
    pass
