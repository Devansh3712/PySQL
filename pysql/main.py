"""
module for running
PySQL Python Wrapper CLI
"""

try:
    import stdiomask
    import time
    import packages.auth as auth
    import packages.ddl_commands as ddl
    import packages.dml_commands as dml
    import data.info as info
    import data.export as export
    import data.imports as imports

except:
    raise Exception("Package Error: modules not setup")

__version__ = "1.0.2"

print(info.ascii_art)
time.sleep(1)

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

        elif user_input.lower() in ["-v", "version"]:
            print(__version__ + "\n")

        elif user_input.lower() == "ddl":
            print(info.data_definition_language)

        elif user_input.lower() == "showdb":
            result = ddl_obj.show_databases()

            if result:
                print(result + "\n")

            else:
                print("[-] Unable to show databases\n")

        elif user_input.lower() == "createdb":
            db_name = input("pysql> Enter database name: ")
            result = ddl_obj.create_database(db_name)

            if result is True:
                print(f"[+] Created database {db_name}\n")

            else:
                print(f"[-] Unable to create database {db_name}\n")

        elif user_input.lower() == "usedb":
            db_name = input("pysql> Enter database name: ")
            result = ddl_obj.use_database(db_name)

            if result is True:
                current_db = db_name
                db_use = True
                print(f"[+] Connected to database {db_name}\n")

            else:
                print(f"[-] Unable to connect to database {db_name}\n")

        elif user_input.lower() == "dropdb":
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
                tb_name = input("pysql> Enter table name: ")
                args = input("pysql> Enter table details: ")
                args = args.split(",")
                result = ddl_obj.create_table(tb_name, args)

                if result is True:
                    print(f"[+] Created table {tb_name}\n")

                else:
                    print(f"[-] Unable to create table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "droptb":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                result = ddl_obj.drop_table(current_db, tb_name)

                if result is True:
                    print(f"[+] Deleted table {tb_name}\n")

                else:
                    print(f"[-] Unable to delete table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "trunctb":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                result = ddl_obj.truncate_table(current_db, tb_name)

                if result is True:
                    print(f"[+] Truncated table {tb_name}\n")

                else:
                    print(f"[-] Unable to truncate table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "desctb":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                result = ddl_obj.desc_table(current_db, tb_name)

                if result:
                    print(result + "\n")

                else:
                    print(f"[-] Unable to display table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "altertb":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                args = input("pysql> Enter arguments: ")
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
                tb_name = input("pysql> Enter table name: ")
                columns = input("pysql> Enter selection columns: ")
                args = input("pysql> Enter arguments: ")
                result = dml_obj.select(current_db, tb_name, columns, args)

                if result:
                    print(result + "\n")

                else:
                    print("[-] Unable to show selected values\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() in ["insert -s", "insert"]:

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                args = input("pysql> Enter values: ")
                result = dml_obj.insert(current_db, tb_name, args)

                if result is True:
                    print(f"[+] Inserted values in table {tb_name}\n")

                else:
                    print(f"[-] Unable to insert value in table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "insert -m":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                num = int(input("pysql> Enter number of records: "))
                flag = True

                for records in range (num):
                    args = input("pysql> Enter values: ")
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
                tb_name = input("pysql> Enter table name: ")
                path = input("pysql> Enter path to CSV file: ")
                result = dml_obj.insert_file(current_db, tb_name, path)

                if result is True:
                    print(f"[+] Inserted values in table {tb_name}\n")

                else:
                    print(f"[-] Unable to insert value in table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "update":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                columns = input("pysql> Enter columns to update: ")
                args = input("pysql> Enter arguments: ")
                result = dml_obj.update(current_db, tb_name, columns, args)

                if result is True:
                    print(f"[+] Updated values in table {tb_name}\n")

                else:
                    print(f"[-] Unable to update values in table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "delete":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                columns = input("pysql> Enter columns to delete: ")
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
            db_name = input("pysql> Enter database name: ")
            path = input("pysql> Enter path to export: ")
            result = exp_obj.export_database(db_name, path)

            if result is True:
                print(f"[+] Exported database {db_name}\n")

            else:
                print(f"[-] Unable to export database {db_name}\n")

        elif user_input.lower() == "exporttb -txt":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_table_txt(current_db, tb_name, path)

                if result is True:
                    print(f"[+] Exported table {tb_name}\n")

                else:
                    print(f"[-] Unable to export table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "exporttb -csv":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_table_csv(current_db, tb_name, path)

                if result is True:
                    print(f"[+] Exported table {tb_name}\n")

                else:
                    print(f"[-] Unable to export table {tb_name}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "exporttb -sql":

            if db_use is True:
                tb_name = input("pysql> Enter table name: ")
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_table_sql(current_db, tb_name, path)

                if result is True:
                    print(f"[+] Exported table {tb_name}\n")

                else:
                    print(f"[-] Unable to export table {tb_name}\n")

            else:
                print(f"[-] No database in use")

        elif user_input.lower() == "exportall -txt":

            if db_use is True:
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_all_txt(current_db, path)

                if result is True:
                    print(f"[+] Exported all tables in {current_db}\n")

                else:
                    print(f"[-] Unable to export tables in {current_db}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "exportall -csv":

            if db_use is True:
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_all_csv(current_db, path)

                if result is True:
                    print(f"[+] Exported all tables in {current_db}\n")

                else:
                    print(f"[-] Unable to export tables in {current_db}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "exportall -sql":

            if db_use is True:
                path = input("pysql> Enter path to export: ")
                result = exp_obj.export_all_sql(current_db, path)

                if result is True:
                    print(f"[+] Exported all tables in {current_db}\n")

                else:
                    print(f"[-] Unable to export tables in {current_db}\n")

            else:
                print(f"[-] No database in use\n")

        elif user_input.lower() == "importdb":
            db_name = input("pysql> Enter database name: ")
            path = input("pysql> Enter path of file: ")
            result = imp_obj.import_database(db_name, path)

            if result is True:
                print(f"[+] Imported to database {db_name}\n")

            else:
                print(f"[-] Unable to import to database {db_name}\n")

        elif user_input.lower() == "importtb":
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
