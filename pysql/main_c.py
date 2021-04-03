"""
module for running
PySQL Python Wrapper CLI
[colored version]
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
    import data.export as export
    import data.imports as imports

except:
    raise Exception("Package Error: modules not setup")

__version__ = "1.0.2"

if platform.system() == "Windows":
    init(convert = True)

print(f"{Fore.LIGHTRED_EX}{info.ascii_art}{Style.RESET_ALL}")
time.sleep(1)

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

        elif user_input.lower() == "ddl":
            print(info.data_definition_language)

        elif user_input.lower() == "showdb":
            result = ddl_obj.show_databases()

            if result:
                print(result + "\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to show databases{Style.RESET_ALL}\n")

        elif user_input.lower() == "createdb":
            db_name = input("pysql> Enter database name: ")
            result = ddl_obj.create_database(db_name)

            if result is True:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Created database {Style.RESET_ALL}{db_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to create database {Style.RESET_ALL}{db_name}\n")

        elif user_input.lower() == "usedb":
            db_name = input("pysql> Enter database name: ")
            result = ddl_obj.use_database(db_name)

            if result is True:
                current_db = db_name
                db_use = True
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Connected to database {Style.RESET_ALL}{db_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to connect to database {Style.RESET_ALL}{db_name}\n")

        elif user_input.lower() == "dropdb":
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
                tb_name = input("pysql> Enter table name: ")
                args = input("pysql> Enter table details: ")
                args = args.split(",")
                result = ddl_obj.create_table(tb_name, args)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Created table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to create table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "droptb":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                result = ddl_obj.drop_table(current_db, tb_name)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Deleted table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to delete table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "trunctb":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                result = ddl_obj.truncate_table(current_db, tb_name)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Truncated table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to truncate table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "desctb":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                result = ddl_obj.desc_table(current_db, tb_name)

                if result:
                    print(result + "\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to display table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "altertb":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                args = input("pysql> Enter arguments: ")
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
                tb_name = input("pysql> Enter table name: ")
                columns = input("pysql> Enter selection columns: ")
                args = input("pysql> Enter arguments: ")
                result = dml_obj.select(current_db, tb_name, columns, args)

                if result:
                    print(result + "\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to show selected values{Style.RESET_ALL}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() in ["insert -s", "insert"]:

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                args = input("pysql> Enter values: ")
                result = dml_obj.insert(current_db, tb_name, args)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Inserted values in table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to insert value in table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "insert -m":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                num = int(input("pysql> Enter number of records: "))
                flag = True

                for records in range (num):
                    args = input("pysql> Enter values: ")
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
                tb_name = input("pysql> Enter table name: ")
                path = input("pysql> Enter path to CSV file: ")
                result = dml_obj.insert_file(current_db, tb_name, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Inserted values in table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to insert value in table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "update":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                columns = input("pysql> Enter columns to update: ")
                args = input("pysql> Enter arguments: ")
                result = dml_obj.update(current_db, tb_name, columns, args)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Updated values in table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to update values in table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "delete":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                columns = input("pysql> Enter columns to delete: ")
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
            db_name = input("pysql> Enter database name: ")
            path = input("pysql> Enter path to export: ")
            result = exp_obj.export_database(db_name, path)

            if result is True:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported database {Style.RESET_ALL}{db_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export database {Style.RESET_ALL}{db_name}\n")

        elif user_input.lower() == "exporttb -txt":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_table_txt(current_db, tb_name, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "exporttb -csv":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_table_csv(current_db, tb_name, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "exporttb -sql":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_table_sql(current_db, tb_name, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported table {Style.RESET_ALL}{tb_name}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export table {Style.RESET_ALL}{tb_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "exportall -txt":

            if db_use is True:
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_all_txt(current_db, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported all tables in {Style.RESET_ALL}{current_db}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export tables in {Style.RESET_ALL}{current_db}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "exportall -csv":

            if db_use is True:
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_all_csv(current_db, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported all tables in {Style.RESET_ALL}{current_db}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export tables in {Style.RESET_ALL}{current_db}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "exportall -sql":

            if db_use is True:
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_all_sql(current_db, path)

                if result is True:
                    print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Exported all tables in {Style.RESET_ALL}{current_db}\n")

                else:
                    print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to export tables in {Style.RESET_ALL}{current_db}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} No database in use{Style.RESET_ALL}\n")

        elif user_input.lower() == "importdb":
            db_name = input("pysql> Enter database name: ")
            path = input("pysql> Enter path of file: ")
            result = imp_obj.import_database(db_name, path)

            if result is True:
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}]{Fore.GREEN} Imported to database {Style.RESET_ALL}{db_name}\n")

            else:
                print(f"[{Fore.RED}-{Style.RESET_ALL}]{Fore.RED} Unable to import to database {Style.RESET_ALL}{db_name}\n")

        elif user_input.lower() == "importtb":
            db_name = input("pysql> Enter database name: ")
            path = input("pysql> Enter path of file: ")
            result = imp_obj.import_table(db_name, path)

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
