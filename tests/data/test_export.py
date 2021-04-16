"""
module for testing export package
of PySQL
"""

import unittest
import pysql.data.export as export
import pathlib
import os
import shutil

# initializing object for Export class of export module
const = export.Export("root", "root")

class TestExport(unittest.TestCase):
    """
    class for testing functions of
    export package
    """

    def test_export_table_json(self):
        """
        Test `export_table_json` function

        Params
        :db:    ->  name of database used
        :table: ->  name of table used
        :path:  ->  path to export

        Returns True if table is exported to
        specified path, else returns False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_table_json("test", "users", f"{directory}/src")
        self.assertEqual(result, True)
        os.remove(f"{directory}/src/users.json")

    def test_export_table_csv(self):
        """
        Test `export_table_csv` function

        Params
        :db:    ->  name of database used
        :table: ->  name of table used
        :path:  ->  path to export

        Returns True if table is exported to
        specified path, else returns False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_table_csv("test", "users", f"{directory}/src")
        self.assertEqual(result, True)
        os.remove(f"{directory}/src/users.csv")

    def test_export_table_sql(self):
        """
        Test `export_table_sql` function

        Params
        :db:    ->  name of database used
        :table: ->  name of table used
        :path:  ->  path to export

        Returns True if table is exported to
        specified path, else returns False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_table_sql("test", "users", f"{directory}/src")
        self.assertEqual(result, True)
        os.remove(f"{directory}/src/test.users.sql")

    def test_export_all_json(self):
        """
        Test `export_all_json` function

        Params
        :db:    ->  name of database used
        :path:  ->  path to export

        Returns True if table is exported to
        specified path, else returns False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_all_json("test", f"{directory}/src")
        self.assertEqual(result, True)
        shutil.rmtree(f"{directory}/src/test")

    def test_export_all_csv(self):
        """
        Test `export_all_csv` function

        Params
        :db:    ->  name of database used
        :path:  ->  path to export

        Returns True if table is exported to
        specified path, else returns False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_all_csv("test", f"{directory}/src")
        self.assertEqual(result, True)
        shutil.rmtree(f"{directory}/src/test")

    def test_export_all_sql(self):
        """
        Test `export_all_sql` function

        Params
        :db:    ->  name of database used
        :path:  ->  path to export

        Returns True if table is exported to
        specified path, else returns False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_all_sql("test", f"{directory}/src")
        self.assertEqual(result, True)
        shutil.rmtree(f"{directory}/src/test")

    def test_export_database(self):
        """
        Test `export_database` function

        Params
        :db:    ->  name of database used
        :path:  ->  path to export

        Returns True if table is exported to
        specified path, else returns False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_database("test", f"{directory}/src")
        self.assertEqual(result, True)
        os.remove(f"{directory}/src/test.sql")


if __name__ == "__main__":
    unittest.main()

"""
PySQL
Devansh Singh, 2021
"""
