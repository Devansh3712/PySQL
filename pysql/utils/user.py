"""
module for maintaining a
default PySQL user
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

try:
    import pysql.utils.exceptions as exceptions
    import pysql.packages.auth as auth
    import dotenv
    from typing import Union

except:
    raise exceptions.ModuleSetupError("user")


class User:
    """
    class for maintaining a default user for
    PySQL
    """

    def __init__(self):
        self.directory = os.path.dirname(os.path.realpath(__file__))

    def add_default_user(self, uname: str, passw: str) -> bool:
        """
        Create a default user login for PySQL

        Parameters
        ----------
        uname: str
            username to be stored
        passw: str
            password to be stored

        Returns
        -------
        bool
            True if .env file is created else False
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
        Checks if a default user is setup

        Returns
        ------
        bool
            True if .env file exists else False
        """
        try:
            # check if file exists
            if os.path.isfile(f"{self.directory}/.env") is True:
                return True

            else:
                return False

        except:
            return False

    def get_default_user(self) -> Union[str, bool]:
        """
        Get the default user credentials

        Returns
        -------
        bool
            True if default user is created else False
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
        Remove default user credentials

        Returns
        -------
        bool
            True if existing .env file is deleted else False
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
