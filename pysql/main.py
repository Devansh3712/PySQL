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


__version__ = "0.0.1"
__author__ = "Devansh Singh"
__email__ = "devanshamity@gmail.com"
__license__ = "MIT"


print(info.ascii_art)
time.sleep(1)

uname = input("Username: ")
passwd = stdiomask.getpass(prompt = "Password: ")
dbname = input("Database: ")

authenticate = auth.Database(uname, passwd, dbname).authenticate()
if authenticate is False:
    print("\n[-]Credentials could not be authenticated")
    exit()

print(f"\n[+]Connected to database {dbname}")
time.sleep(1)

print(info.menu)

while (True):

    user_input = input("pysql> ")
    ddl_obj = ddl.DDL(uname, passwd, dbname)
    dml_obj = dml.DML(uname, passwd, dbname)
    exp_obj = export.Export(uname, passwd, dbname)
    imp_obj = imports.Import(uname, passwd, dbname)

    if user_input.lower() in ["-a", "about"]:
        print(info.about)

    elif user_input.lower() in ["-h", "help"]:
        print(info.menu)

    elif user_input.lower() in ["-q", "quit"]:
        print("Goodbye")
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

    elif user_input.lower() == "dropdb":
        db_name = input("pysql> Enter database name: ")

        if db_name == dbname:
            print("[-]Cannot delete database in use\n")

        else:
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
        tb_name = input("pysql> Enter table name: ")
        args = input("pysql> Enter table details: ")
        args = args.split(",")
        result = ddl_obj.create_table(tb_name, args)

        if result is True:
            print(f"[+]Created table {tb_name}\n")

        else:
            print(f"[-]Unable to create table {tb_name}\n")

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
        print(info.data_manipulation_language)

    elif user_input.lower() == "select":
        tb_name = input("pysql> Enter table name: ")
        columns = input("pysql> Enter selection columns: ")
        args = input("pysql> Enter arguments: ")
        result = dml_obj.select(tb_name, columns, args)

        if result:
            print(result + "\n")

        else:
            print("[-]Unable to show selected values\n")

    elif user_input.lower() in ["insert -s", "insert"]:
        tb_name = input("pysql> Enter table name: ")
        args = input("pysql> Enter values: ")
        result = dml_obj.insert(tb_name, args)

        if result is True:
            print(f"[+]Inserted values in table {tb_name}\n")

        else:
            print(f"[-]Unable to insert value in table {tb_name}\n")

    elif user_input.lower() == "insert -m":
        tb_name = input("pysql> Enter table name: ")
        num = int(input("pysql> Enter number of records: "))

        for records in range (num):
            args = input("pysql> Enter values: ")
            result = dml_obj.insert(tb_name, args)

            if result is False:
                print(f"[-]Unable to insert value in table {tb_name}\n")
                break

        print(f"[+]Inserted values in table {tb_name}\n")

    elif user_input.lower() == "insert -f":
        tb_name = input("pysql> Enter table name: ")
        path = input("pysql> Enter path to CSV file: ")
        result = dml_obj.insert_file(tb_name, path)

        if result is True:
            print(f"[+]Inserted values in table {tb_name}\n")

        else:
            print(f"[-]Unable to insert value in table {tb_name}\n")

    elif user_input.lower() == "update":
        tb_name = input("pysql> Enter table name: ")
        columns = input("pysql> Enter columns to update: ")
        args = input("pysql> Enter arguments: ")
        result = dml_obj.update(tb_name, columns, args)

        if result is True:
            print(f"[+]Updated values in table {tb_name}\n")

        else:
            print(f"[-]Unable to update values in table {tb_name}\n")

    elif user_input.lower() == "delete":
        tb_name = input("pysql> Enter table name: ")
        columns = input("pysql> Enter columns to delete: ")
        result = dml_obj.delete(tb_name, columns)

        if result is True:
            print(f"[+]Deleted values from table {tb_name}\n")

        else:
            print(f"[-]Unable to delete values from table {tb_name}\n")

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
            print(f"[+]Exported database {db_name}\n")

        else:
            print(f"[-]Unable to export database {db_name}\n")

    elif user_input.lower() == "exporttb -txt":
        tb_name = input("pysql> Enter table name: ")
        path = input("pysql> Enter path to export: ")
        result = exp_obj.export_table_txt(tb_name, path)

        if result is True:
            print(f"[+]Exported table {tb_name}\n")

        else:
            print(f"[-]Unable to export table {tb_name}\n")

    elif user_input.lower() == "exporttb -csv":
        tb_name = input("pysql> Enter table name: ")
        path = input("pysql> Enter path to export: ")
        result = exp_obj.export_table_csv(tb_name, path)

        if result is True:
            print(f"[+]Exported table {tb_name}\n")

        else:
            print(f"[-]Unable to export table {tb_name}\n")

    elif user_input.lower() == "exporttb -sql":
        db_name = input("pysql> Enter database name: ")
        tb_name = input("pysql> Enter table name: ")
        path = input("pysql> Enter path to export: ")
        result = exp_obj.export_table_sql(db_name, tb_name, path)

        if result is True:
            print(f"[+]Exported table {tb_name}\n")

        else:
            print(f"[-]Unable to export table {tb_name}\n")

    elif user_input.lower() == "exportall -txt":
        path = input("pysql> Enter path to export: ")
        result = exp_obj.export_all_txt(path)

        if result is True:
            print(f"[+]Exported all tables in {dbname}\n")

        else:
            print(f"[-]Unable to export tables in {dbname}\n")

    elif user_input.lower() == "exportall -csv":
        path = input("pysql> Enter path to export: ")
        result = exp_obj.export_all_csv(path)

        if result is True:
            print(f"[+]Exported all tables in {dbname}\n")

        else:
            print(f"[-]Unable to export tables in {dbname}\n")

    elif user_input.lower() == "exportall -sql":
        path = input("pysql> Enter path to export: ")
        result = exp_obj.export_all_sql(path)

        if result is True:
            print(f"[+]Exported all tables in {dbname}\n")

        else:
            print(f"[-]Unable to export tables in {dbname}\n")

    elif user_input.lower() == "importdb":
        db_name = input("pysql> Enter database name: ")
        path = input("pysql> Enter path of file: ")
        result = imp_obj.import_database(db_name, path)

        if result is True:
            print(f"[+]Imported to database {db_name}\n")

        else:
            print(f"[-]Unable to import to database {db_name}\n")

    elif user_input.lower() == "importtb":
        db_name = input("pysql> Enter database name: ")
        path = input("pysql> Enter path of file: ")
        result = imp_obj.import_table(db_name, path)

        if result is True:
            print(f"[+]Imported table to database {db_name}\n")

        else:
            print(f"[-]Unable to import table to database {db_name}\n")

    else:
        print("Choose a valid option")


"""
PySQL
Devansh Singh, 2021
"""
