"""
module for testing imports package
of PySQL
"""

import unittest
import pathlib
import pysql.data.imports as imports
import pysql.packages.ddl_commands as ddl_commands

ddl = ddl_commands.DDL("root", "root")
const = imports.Import("root", "root")

class TestImports(unittest.TestCase):
    """
    class for testing functions of
    imports package
    """

    def test_import_database(self):
        """
        Test `import_database` function

        Params
        :db:    ->  name of database to import
        :path:  ->  path of file
        """
        directory = pathlib.Path(__file__).parents[2]
        ddl.create_database("test_two")
        result = const.import_database("test_two", f"{directory}/src/import_db.sql")
        self.assertEqual(result, True)
        ddl.drop_database("test_two")

    def test_import_table(self):
        """
        Test `import_table` function

        Params
        :db:    ->  name of database to import
        :path:  ->  path of file
        """
        directory = pathlib.Path(__file__).parents[2]
        ddl.create_database("test_two")
        result = const.import_table("test_two", f"{directory}/src/import_tb.sql")
        self.assertEqual(result, True)
        ddl.drop_database("test_two")


if __name__ == "__main__":
    unittest.main()

"""
PySQL
Devansh Singh, 2021
"""
