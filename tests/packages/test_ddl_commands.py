"""
module for testing ddl_commands package
of PySQL
"""

import unittest
import pysql.packages.ddl_commands as ddl_commands

# initializing objects for classes of ddl_commands
const = ddl_commands.DDL("root", "root")
aconst = ddl_commands.Alter("root", "root", "test", "users")

class TestDDL_Commands(unittest.TestCase):
    """
    class for testing functions of DDL
    class of ddl_commands package
    """

    def test_create_database(self):
        """
        Test `create_database` function

        Params
        :database:  ->  name of database to be
                        created

        Returns True if database is created in
        MySQL server, else returns False
        """
        result = const.create_database("test_db")
        self.assertEqual(result, True)
        const.drop_database("test_db")

    def test_use_database(self):
        """
        Test `use_database` function

        Params
        :database:  ->  name of database to be used

        Returns True if database can be used,
        else returns False
        """
        const.create_database("test_db")
        result = const.use_database("test_db")
        self.assertEqual(result, True)
        const.drop_database("test_db")

    def test_drop_database(self):
        """
        Test `drop_database` function

        Params
        :database:  ->  name of database to be
                        created

        Returns True if database is deleted in
        MySQL server, else returns False
        """
        const.create_database("test_db")
        result = const.drop_database("test_db")
        self.assertEqual(result, True)

    def test_create_table(self):
        """
        Test `create_table` function

        Params
        :db:    ->  name of database used
        :table: ->  name of table to be created
        :args:  ->  arguments (columns & type)

        Returns True if table is created in used
        database, else returns False
        """
        result = const.create_table("test", "test_tb", ["name varchar(30)"])
        self.assertEqual(result, True)
        const.drop_table("test", "test_tb")

    def test_drop_table(self):
        """
        Test `drop_table` function

        Params
        :db:    ->  name of database used
        :table: ->  name of table to be deleted

        Returns True if table is deleted in used
        database, else returns False
        """
        const.create_table("test", "test_tb", ["name varchar(30)"])
        result = const.drop_table("test", "test_tb")
        self.assertEqual(result, True)

    def test_truncate_table(self):
        """
        Test `truncate_table` function

        Params
        :db:    ->  name of database used
        :table: ->  name of table to be truncated

        Returns True if table is truncated in used
        database, else returns False
        """
        const.create_table("test", "test_tb", ["name varchar(30)"])
        result = const.truncate_table("test", "test_tb")
        self.assertEqual(result, True)
        const.drop_table("test", "test_tb")

    def test_alter_table(self):
        """
        Test `alter_table` function

        Params
        :db:    ->  name of database used
        :table: ->  name of table to alter
        :args:  ->  arguments (add/modify/drop, column & type)

        Returns True if table schema is altered,
        else returns False
        """
        const.create_table("test", "test_tb", ["name varchar(30)"])
        result1 = const.alter_table("test", "test_tb", ["add", "age char(2)"])
        self.assertEqual(result1, True)
        result2 = const.alter_table("test", "test_tb", ["modify", "age int"])
        self.assertEqual(result2, True)
        result3 = const.alter_table("test", "test_tb", ["drop", "age"])
        self.assertEqual(result3, True)
        const.drop_table("test", "test_tb")


class TestAlter(unittest.TestCase):
    """
    class for testing functions of Alter
    class of ddl_commands package
    """

    def test_add_column(self):
        """
        Test `add_column` function

        Params
        :column:    ->  column name & type to be added

        Returns True if column is added to the table,
        else returns False
        """
        result = aconst.add_column("num char(10)")
        self.assertEqual(result, True)
        aconst.drop_column("num")

    def test_modify_column(self):
        """
        Test `modify_column` function

        Params
        :column:    ->  column name & type to be modified

        Returns True if column is modified,
        else returns False
        """
        aconst.add_column("num char(10)")
        result = aconst.modify_column("num int")
        self.assertEqual(result, True)
        aconst.drop_column("num")

    def test_drop_column(self):
        """
        Test `drop_column` function

        Params
        :column:    ->  column name to be deleted

        Returns True if column is deleted from table,
        else returns False
        """
        aconst.add_column("num char(10)")
        result = aconst.drop_column("num")
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()

"""
PySQL
Devansh Singh, 2021
"""
