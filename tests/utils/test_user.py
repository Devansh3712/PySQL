"""
module for testing user package
of PySQL
"""

import unittest
import pysql.utils.user as user

# instance object for user module
const = user.User()

class TestUser(unittest.TestCase):
    """
    class for testing functions of
    user package
    """

    def test_add_default_user(self):
        """
        Test `add_default_user` function

        Params
        :uname: ->  MySQL username
        :passw: ->  MySQL password

        Returns True if default user is created,
        else returns False
        """
        result = const.add_default_user("root", "root")
        self.assertEqual(result, True)
        const.remove_default_user()

    def test_check_default_user(self):
        """
        Test `check_default_user` function

        Returns True if `.env` file exists, else
        returns False
        """
        const.add_default_user("root", "root")
        result = const.check_default_user()
        self.assertEqual(result, True)
        const.remove_default_user()

    def test_get_default_user(self):
        """
        Test `get_default_user` function

        Returns credentials if `.env` file exists, else
        returns False
        """
        const.add_default_user("root", "root")
        result = const.get_default_user()
        self.assertEqual(result, ["root", "root"])
        const.remove_default_user()

    def test_remove_default_user(self):
        """
        Test `remove_default_user` function

        Returns True if default user is deleted,
        else returns False
        """
        const.add_default_user("root", "root")
        result = const.remove_default_user()
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()

"""
PySQL
Devansh Singh, 2021
"""
