"""
module for running
PySQL Python Wrapper CLI
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

try:
    import pysql.utils.exceptions as exceptions
    import stdiomask
    import time
    import urllib.request
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

print(info.ascii_art)
time.sleep(1)

# check if a default user exists
check = user.User().check_default_user()

if check is True:
    # get default user's name
    def_user = user.User().get_default_user()
    print(f"\n[+] Default user {def_user[0]} authenticated")
    uname = def_user[0]
    passwd = def_user[1]

else:
    uname = input("Username: ")
    passwd = stdiomask.getpass(prompt = "Password: ")

    # authenticate input credentials
    authenticate = auth.Database(uname, passwd).authenticate()
    if authenticate is False:
        print("\n[-] User could not be authenticated")
        exit()

    print(f"\n[+] User authenticated")

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
        user_input = input(f"({current_db}) pysql> ")

    else:
        user_input = input("pysql> ")

    try:

        if user_input.lower() in ["-a", "about"]:
            print(info.about)

        elif user_input.lower() in ["-h", "help"]:
            print(info.menu)

        elif user_input.lower() in ["-q", "quit"]:
            print("Goodbye")
            break

        elif user_input.lower() in ["-c", "commands"]:
            print(info.commands)

        elif user_input.lower() in ["-d", "def user"]:
            print(info.default_user)

        elif user_input.lower() in ["-v", "version"]:
            print(__version__ + "\n")

        elif user_input.lower() in ["-u", "updates"]:
            gh_version = urllib.request.urlopen("https://raw.githubusercontent.com/Devansh3712/PySQL/main/pysql/__version__.py")
            gh_version = gh_version.read().decode("utf-8")

            if gh_version > __version__:

                result = update.update_pysql()

                if result is True:
                    print(f"[+] PySQL updated to v{gh_version} succesfully\n")
                    break

                else:
                    print(f"[-] Unable to update PySQL\n")

            else:
                print(f"[+] PySQL is up-to-date\n")

        elif user_input.lower() == "adduser":

            if db_use is True:
                _uname = input(f"({current_db}) pysql> Enter username: ")
                _passwd = stdiomask.getpass(prompt = f"({current_db}) pysql> Enter password: ")

            else:
                _uname = input("pysql> Enter username: ")
                _passwd = stdiomask.getpass(prompt = "pysql> Enter password: ")

            result = user.User().add_default_user(_uname, _passwd)

            if result is True:
                print(f"[+] Default user {_uname} created\n")

            else:
                print(f"[-] Unable to create default user\n")

        elif user_input.lower() == "removeuser":

            if db_use is True:
                _passwd = stdiomask.getpass(prompt = f"({current_db}) pysql> Enter password: ")

            else:
                _passwd = stdiomask.getpass(prompt = "pysql> Enter password: ")

            def_user = user.User().get_default_user()
            if _passwd == def_user[1]:
                result = user.User().remove_default_user()

                if result is True:
                    print(f"[+] Default user {def_user[0]} removed\n")

                else:
                    print(f"[-] Unable to remove default user\n")

            else:
                print("[-] Unable to authenticate\n")

        elif user_input.lower() == "ddl":
            print(info.data_definition_language)

        elif user_input.lower() == "showdb":
            result = ddl_obj.show_databases()

            if result:
                print(result + "\n")

            else:
                print("[-] Unable to show databases\n")

        elif user_input.lower() == "createdb":

            if db_use is True:
                db_name = input(f"({current_db}) pysql> Enter database name: ")

            else:
                db_name = input("pysql> Enter database name: ")

            result = ddl_obj.create_database(db_name)

            if result is True:
                print(f"[+] Created database {db_name}\n")

            else:
                print(f"[-] Unable to create database {db_name}\n")

        elif user_input.lower() == "usedb":

            if db_use is True:
                db_name = input(f"({current_db}) pysql> Enter database name: ")

            else:
                db_name = input("pysql> Enter database name: ")

            result = ddl_obj.use_database(db_name)

            if result is True:
                current_db = db_name
                db_use = True
                print(f"[+] Connected to database {db_name}\n")

            else:
                print(f"[-] Unable to connect to database {db_name}\n")

        elif user_input.lower() == "dropdb":

            if db_use is True:
                db_name = input(f"({current_db}) pysql> Enter database name: ")

            else:
                db_name = input("pysql> Enter database name: ")

            result = ddl_obj.drop_database(db_name)

            if result is True:
                print(f"[+] Deleted database {db_name}\n")
                current_db = ""
                db_use = False

            else:
                print(f"[-] Unable to delete database {db_name}\n")

        elif user_input.lower() == "showtb":

            if db_use is True:
                result = ddl_obj.show_tables()

                if result:
                    print(result + "\n")

                else:
                    print("[-] Unable to show tables\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "createtb":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                args = input(f"({current_db}) pysql> Enter table details: ")
                args = args.split(",")
                result = ddl_obj.create_table(current_db, tb_name, args)

                if result is True:
                    print(f"[+] Created table {tb_name}\n")

                else:
                    print(f"[-] Unable to create table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "droptb":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                result = ddl_obj.drop_table(current_db, tb_name)

                if result is True:
                    print(f"[+] Deleted table {tb_name}\n")

                else:
                    print(f"[-] Unable to delete table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "trunctb":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                result = ddl_obj.truncate_table(current_db, tb_name)

                if result is True:
                    print(f"[+] Truncated table {tb_name}\n")

                else:
                    print(f"[-] Unable to truncate table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "desctb":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                result = ddl_obj.desc_table(current_db, tb_name)

                if result:
                    print(result + "\n")

                else:
                    print(f"[-] Unable to display table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "altertb":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                args = input(f"({current_db}) pysql> Enter arguments: ")
                args = args.split(",")
                result = ddl_obj.alter_table(current_db, tb_name, args)

                if result is True:
                    print(f"[+] Altered table {tb_name}\n")

                else:
                    print(f"[-] Unable to alter table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "dml":
            print(info.data_manipulation_language)

        elif user_input.lower() == "select":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                columns = input(f"({current_db}) pysql> Enter selection columns: ")
                args = input(f"({current_db}) pysql> Enter arguments: ")
                result = dml_obj.select(current_db, tb_name, columns, args)

                if result:
                    print(result + "\n")

                else:
                    print("[-] Unable to show selected values\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() in ["insert -s", "insert"]:

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                args = input(f"({current_db}) pysql> Enter values: ")
                result = dml_obj.insert(current_db, tb_name, args)

                if result is True:
                    print(f"[+] Inserted values in table {tb_name}\n")

                else:
                    print(f"[-] Unable to insert value in table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "insert -m":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                num = int(input(f"({current_db}) pysql> Enter number of records: "))
                flag = True

                for records in range (num):
                    args = input(f"({current_db}) pysql> Enter values: ")
                    result = dml_obj.insert(current_db, tb_name, args)

                    if result is False:
                        print(f"[-] Unable to insert value in table {tb_name}\n")
                        flag = False
                        break

                if flag is True:
                    print(f"[+] Inserted values in table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "insert -f":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                path = input(f"({current_db}) pysql> Enter path to CSV file: ")
                result = dml_obj.insert_file(current_db, tb_name, path)

                if result is True:
                    print(f"[+] Inserted values in table {tb_name}\n")

                else:
                    print(f"[-] Unable to insert value in table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "update":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                columns = input(f"({current_db}) pysql> Enter columns to update: ")
                args = input(f"({current_db}) pysql> Enter arguments: ")
                result = dml_obj.update(current_db, tb_name, columns, args)

                if result is True:
                    print(f"[+] Updated values in table {tb_name}\n")

                else:
                    print(f"[-] Unable to update values in table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "delete":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                columns = input(f"({current_db}) pysql> Enter columns to delete: ")
                result = dml_obj.delete(current_db, tb_name, columns)

                if result is True:
                    print(f"[+] Deleted values from table {tb_name}\n")

                else:
                    print(f"[-] Unable to delete values from table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "all":
            print(info.all_commands)

        elif user_input.lower() == "export":
            print(info.export)

        elif user_input.lower() == "import":
            print(info.import_)

        elif user_input.lower() == "exportdb":

            if db_use is True:
                db_name = input(f"({current_db}) pysql> Enter database name: ")
                path = input(f"({current_db}) pysql> Enter path to export: ")

            else:
                db_name = input("pysql> Enter database name: ")
                path = input("pysql> Enter path to export: ")

            result = exp_obj.export_database(db_name, path)

            if result is True:
                print(f"[+] Exported database {db_name}\n")

            else:
                print(f"[-] Unable to export database {db_name}\n")

        elif user_input.lower() == "exporttb -json":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                path = input(f"({current_db}) pysql> Enter path to export: ")
                result = exp_obj.export_table_json(current_db, tb_name, path)

                if result is True:
                    print(f"[+] Exported table {tb_name}\n")

                else:
                    print(f"[-] Unable to export table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "exporttb -csv":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                path = input(f"({current_db}) pysql> Enter path to export: ")
                result = exp_obj.export_table_csv(current_db, tb_name, path)

                if result is True:
                    print(f"[+] Exported table {tb_name}\n")

                else:
                    print(f"[-] Unable to export table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "exporttb -sql":

            if db_use is True:
                tb_name = input(f"({current_db}) pysql> Enter table name: ")
                path = input(f"({current_db}) pysql> Enter path to export: ")
                result = exp_obj.export_table_sql(current_db, tb_name, path)

                if result is True:
                    print(f"[+] Exported table {tb_name}\n")

                else:
                    print(f"[-] Unable to export table {tb_name}\n")

            else:
                print(f"[-] No database in use")

        elif user_input.lower() == "exportall -json":

            if db_use is True:
                path = input(f"({current_db}) pysql> Enter path to export: ")
                result = exp_obj.export_all_json(current_db, path)

                if result is True:
                    print(f"[+] Exported all tables in {current_db}\n")

                else:
                    print(f"[-] Unable to export tables in {current_db}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "exportall -csv":

            if db_use is True:
                path = input(f"({current_db}) pysql> Enter path to export: ")
                result = exp_obj.export_all_csv(current_db, path)

                if result is True:
                    print(f"[+] Exported all tables in {current_db}\n")

                else:
                    print(f"[-] Unable to export tables in {current_db}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "exportall -sql":

            if db_use is True:
                path = input(f"({current_db}) pysql> Enter path to export: ")
                result = exp_obj.export_all_sql(current_db, path)

                if result is True:
                    print(f"[+] Exported all tables in {current_db}\n")

                else:
                    print(f"[-] Unable to export tables in {current_db}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "importdb":

            if db_use is True:
                db_name = input(f"({current_db}) pysql> Enter database name: ")
                path = input(f"({current_db}) pysql> Enter path of file: ")

            else:
                db_name = input("pysql> Enter database name: ")
                path = input("pysql> Enter path of file: ")

            result = imp_obj.import_database(db_name, path)

            if result is True:
                print(f"[+] Imported to database {db_name}\n")

            else:
                print(f"[-] Unable to import to database {db_name}\n")

        elif user_input.lower() == "importtb":

            if db_use is True:
                db_name = input(f"({current_db}) pysql> Enter database name: ")
                path = input(f"({current_db}) pysql> Enter path of file: ")

            else:
                db_name = input("pysql> Enter database name: ")
                path = input("pysql> Enter path of file: ")

            result = imp_obj.import_table(db_name, path)

            if result is True:
                print(f"[+] Imported table to database {db_name}\n")

            else:
                print(f"[-] Unable to import table to database {db_name}\n")

        else:
            print("[-] Choose a valid option\n")

    except:
        print(f"[-] Unable to execute command\n")

# entry point for running PySQL CLI
def cli():
    pass


"""
PySQL
Devansh Singh, 2021
"""
