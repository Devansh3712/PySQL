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
        Test export_table_json function

        Parameters
        ----------
        db: str
            name of database to use
        table: str
            name of table to export
        path: str
            path to export table
        
        Returns
        -------
        bool
            True if table is exported else False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_table_json("test", "users", os.path.join(directory, "src"))
        self.assertEqual(result, True)
        os.remove(os.path.join(directory, "src", "users.json"))

    def test_export_table_csv(self):
        """
        Test export_table_csv function

        Parameters
        ----------
        db: str
            name of database to use
        table: str
            name of table to export
        path: str
            path to export table
        
        Returns
        -------
        bool
            True if table is exported else False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_table_csv("test", "users", os.path.join(directory, "src"))
        self.assertEqual(result, True)
        os.remove(os.path.join(directory, "src", "users.csv"))

    def test_export_table_sql(self):
        """
        Test export_table_sql function

        Parameters
        ----------
        db: str
            name of database to use
        table: str
            name of table to export
        path: str
            path to export SQL file
        
        Returns
        -------
        bool
            True if table is exported else False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_table_sql("test", "users", os.path.join(directory, "src"))
        self.assertEqual(result, True)
        os.remove(os.path.join(directory, "src", "test.users.sql"))

    def test_export_all_json(self):
        """
        Test export_all_json function

        Parameters
        ----------
        db: str
            name of database to use
        path: str
            path to export tables
        
        Returns
        -------
        bool
            True if tables are exported else False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_all_json("test", os.path.join(directory, "src"))
        self.assertEqual(result, True)
        shutil.rmtree(os.path.join(directory, "src", "test"))

    def test_export_all_csv(self):
        """
        Test export_all_csv function

        Parameters
        ----------
        db: str
            name of database to use
        path: str
            path to export tables
        
        Returns
        -------
        bool
            True if tables are exported else False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_all_csv("test", os.path.join(directory, "src"))
        self.assertEqual(result, True)
        shutil.rmtree(os.path.join(directory, "src", "test"))

    def test_export_all_sql(self):
        """
        Test export_all_sql function

        Parameters
        ----------
        db: str
            name of database to use
        path: str
            path to export tables
        
        Returns
        -------
        bool
            True if tables are exported else False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_all_sql("test", os.path.join(directory, "src"))
        self.assertEqual(result, True)
        shutil.rmtree(os.path.join(directory, "src", "test"))

    def test_export_database(self):
        """
        Test export_database function

        Parameters
        ----------
        db: str
            name of database to export
        path: str
            path to export SQL file
        
        Returns
        -------
        bool
            True if database is exported else False
        """
        directory = pathlib.Path(__file__).parents[2]
        result = const.export_database("test", os.path.join(directory, "src"))
        self.assertEqual(result, True)
        os.remove(os.path.join(directory, "src", "test"))


if __name__ == "__main__":
    unittest.main()

"""
PySQL
Devansh Singh, 2021
"""
