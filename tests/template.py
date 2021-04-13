"""
module for creating template for
testing PySQL modules
"""

import datetime
import os
import sys
import pathlib

# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

module = input("Enter module name: ")
folder = input("Enter folder name: ")
author = input("Enter author name: ")

template = f'''"""
module for testing {module} package
of PySQL
"""

import unittest
import pysql.{folder}.{module} as {module}

class Test{module.title()}(unittest.TestCase):
    """
    class for testing functions of
    {module} package
    """



if __name__ == "__main__":
    unittest.main()

"""
PySQL
{author}, {datetime.datetime.now().strftime("%Y")}
"""
'''

file = open(f"{pathlib.Path(__file__).parent.absolute()}/{folder}/test_{module}.py", "w")
file.write(template)
file.close()


"""
PySQL
Devansh Singh, 2021
"""
