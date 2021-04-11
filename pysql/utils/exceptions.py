"""
module for custom exceptions
for PySQL
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

class PySQLPackageError(Exception):
    """
    Exception raised for errors in running modules
    of PySQL
    """

    def __init__(self):

        self.message = "Modules not setup for PySQL"
        super().__init__(self.message)


class AuthenticationError(Exception):
    """
    Exception raised for error in MySQL user
    authentication
    """

    def __init__(self):

        self.message = "User cannot be authenticated"
        super().__init__(self.message)


class ModuleSetupError(Exception):
    """
    Exception raised for error in running
    a particular module

    :module:    ->  name of module
    """

    def __init__(self, module: str):

        self.module = module
        self.message = "module not setup"
        super().__init__(self.message)

    def __str__(self):
        return f"'{self.module}' {self.message}"


"""
PySQL
Devansh Singh, 2021
"""
