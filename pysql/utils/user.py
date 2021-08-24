"""
module for maintaining a
default user
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

try:
    import pysql.utils.exceptions as exceptions
    import dotenv
    import pysql.packages.auth as auth

except:
    raise exceptions.ModuleSetupError("user")


class User:
    """
    class for maintaining a default user for
    PySQL

    :add_default_user:      ->  create a `default user` for
                                PySQL direct login, if username
                                and password are valid
                                [returns boolean value]

    :check_default_user:    ->  checks if an `.env` file is present
                                in the current directory
                                [returns boolean value]

    :get_default_user:      ->  if `.env` file exists, gets the
                                default user credentials
                                [returns default user else False]

    :remove_default_user:   ->  if `.env` file exists, deletes the
                                file and its contents
                                [returns boolean value]
    """

    def __init__(self):
        self.directory = os.path.dirname(os.path.realpath(__file__))

    def add_default_user(self, uname: str, passw: str) -> bool:
        """
        Create a default user login for PySQL, returns
        True if `.env` file is created else False

        uname   ->  username to be stored
        passwd  ->  password to be stored
        """
        # authenticate user credentials
        authenticate = auth.Database(uname, passw).authenticate()

        try:
            if (authenticate is True):

                # create an environment file
                file = open(f"{self.directory}/.env", "w")
                # add user credentials to .env file
                file.write(f'UNAME="{uname}"' + "\n")
                file.write(f'PASSWD="{passw}"' + "\n")
                file.close()

                return True

            else:
                return False

        except:
            return False

    def check_default_user(self) -> bool:
        """
        Checks if a default user is setup, i.e
        returns True if `.env` file exists in 
        `utils` directory else False
        """
        try:
            # check if file exists
            if os.path.isfile(f"{self.directory}/.env") is True:
                return True

            else:
                return False

        except:
            return False

    def get_default_user(self):
        """
        If a default user is setup, returns
        the user credentials else False
        """
        try:
            if User().check_default_user() is True:

                dotenv.load_dotenv(f"{self.directory}/.env")
                # load default user credentials
                username = os.environ.get("UNAME")
                password = os.environ.get("PASSWD")
                result = [username, password]

                return result

            else:
                return False

        except:
            return False

    def remove_default_user(self) -> bool:
        """
        If a default user is setup, deletes
        the `.env` file and its contents and
        returns True else False
        """
        try:
            if User().check_default_user() is True:

                # delete the .env file
                os.remove(f"{self.directory}/.env")
                return True

            else:
                return False

        except:
            return False


"""
PySQL
Devansh Singh, 2021
"""
