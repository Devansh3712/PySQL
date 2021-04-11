"""
module for testing auth package
of PySQL
"""

import unittest
import pysql.packages.auth as auth

class TestAuth(unittest.TestCase):
    """
    class for testing functions of
    auth package
    """

    def test_authenticate(self):
        """
        Test `authenticate` function

        Returns True if connection with MySQL
        server can be made, else returns
        False
        """

        result = auth.Database("root", "root").authenticate()
        self.assertEqual(result, True)

    def test_auth_db(self):
        """
        Test `auth_db` function

        Params
        :database:  ->  name of database to authenticate

        Returns True if database exists in MySQL
        server, else returns False
        """

        result = auth.Database("root", "root").auth_db("test")
        self.assertEqual(result, True)

    def test_auth_table(self):
        """
        Test `auth_table` function

        Params
        :database:  ->  name of database
        :table:     ->  name of table to authenticate

        Returns True if table exists in database,
        else returns False
        """

        result = auth.Database("root", "root").auth_table("test", "users")
        self.assertEqual(result, True)

    def test_auth_table_columns(self):
        """
        Test `auth_table_columns` function

        Params
        :database:  ->  name of database
        :table:     ->  name of table to authenticate
        :query:     ->  name & type of column
        """

        result = auth.Database("root", "root").auth_table_columns("test", "users", "name varchar(30)")
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()

"""
PySQL
Devansh Singh, 2021
"""
