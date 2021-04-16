"""
module for updating PySQL
through pip/GitHub
"""

import os
import sys
# create relative path for importing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import platform
from subprocess import call, STDOUT

def update_pysql() -> bool:

    try:
        if platform.system() == "Windows":

            # creates a text file with a list of all installed modules
            os.system("pip freeze > dependencies.txt")
            file = open("dependencies.txt").read().splitlines()
            flag = False

            for module in file:

                module = module.split("==")

                if module[0] == "pysql-cli":
                    os.system("pip install pysql-cli --upgrade >> NUL 2>&1")
                    os.remove("dependencies.txt")
                    flag = True
                    return True

            if flag is False:

                os.remove("dependencies.txt")

                # checks if the current directory is a git repository
                if call(["git", "branch"], stderr = STDOUT, stdout = open(os.devnull, "w")) != 0:
                    return False

                else:
                    os.system("git pull >> NUL 2>&1")
                    return True

        else:

            # creates a text file with a list of all installed modules
            os.system("pip3 freeze > dependencies.txt")
            file = open("dependencies.txt").read().splitlines()
            flag = False

            for module in file:

                module = module.split("==")

                if module[0] == "pysql-cli":
                    os.system("pip3 install pysql-cli --upgrade >> /dev/null 2>&1")
                    os.remove("dependencies.txt")
                    flag = True
                    return True

            if flag is False:

                os.remove("dependencies.txt")

                # checks if the current directory is a git repository
                if call(["git", "branch"], stderr = STDOUT, stdout = open(os.devnull, "w")) != 0:
                    return False

                else:
                    os.system("git pull >> /dev/null 2>&1")
                    return True

    except:
        return False


"""
PySQL
Devansh Singh, 2020
"""
