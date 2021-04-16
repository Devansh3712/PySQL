"""
module for testing dml_commands package
of PySQL
"""

import unittest
import pysql.packages.dml_commands as dml_commands
import pathlib

# initializing object for DML class of dml_commands
const = dml_commands.DML("root", "root")

class TestDML_Commands(unittest.TestCase):
    """
    class for testing functions of
    dml_commands package
    """

    def test_insert(self):
        """
        Test `insert` function

        Params
        :db:    ->  name of database used
        :table: ->  name of table used
        :args:  ->  arguments (values to be inserted)

        Returns True if data is inserted into
        table, else returns False
        """
        result = const.insert("test", "users", "Ammo,16,22/01")
        self.assertEqual(result, True)
        const.delete("test", "users", "name='Ammo'")

    def test_insert_file(self):
        """
        Test `insert_file` function

        Params
        :db:        ->  name of database used
        :table:     ->  name of table used
        :file_path: ->  path to CSV file

        Returns True if data is inserted into
        table from CSV file, else returns False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.insert_file("test", "users", f"{directory}/src/test.csv")
        self.assertEqual(result, True)
        const.delete("test", "users", "name='Ammo'")

    def test_update(self):
        """
        Test `update` function

        Params
        :db:        ->  name of database used
        :table:     ->  name of table used
        :columns:   ->  name of column to be updated
        :args:      ->  arguments

        Returns True if data is updated in the table,
        else returns False
        """
        result = const.update("test", "users", "age=18", "name='Preetika'")
        self.assertEqual(result, True)
        const.update("test", "users", "age=17", "name='Preetika'")

    def test_delete(self):
        """
        Test `delete` function

        Params
        :db:        ->  name of database used
        :table:     ->  name of table used  
        :column:    ->  column and argument

        Returns True if data is deleted from the table,
        else returns False
        """
        const.insert("test", "users", "Ammo,16,22/01")
        result = const.delete("test", "users", "name='Ammo'")
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()

"""
PySQL
Devansh Singh, 2021
"""
