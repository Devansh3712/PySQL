"""
module for updating PySQL
through pip/GitHub
"""

import os
import platform
from subprocess import call, STDOUT

def update_pysql() -> bool:

    try:
        if platform.system() == "Windows":

            os.system("pip freeze > dependencies.txt")
            file = open("dependencies.txt").read().splitlines()
            flag = False

            for module in file:

                module = module.split("==")

                if module[0] == "pysql-cli":
                    os.system("pip install pysql-cli --upgrade")
                    flag = True
                    return True

            if flag is False:

                if call(["git", "branch"], stderr = STDOUT, stdout = open(os.devnull, "w")) != 0:
                    return False

                else:
                    os.system("git pull")
                    return True

        else:

            os.system("pip3 freeze > dependencies.txt")
            file = open("dependencies.txt").read().splitlines()
            flag = False

            for module in file:

                module = module.split("==")

                if module[0] == "pysql-cli":
                    os.system("pip3 install pysql-cli --upgrade")
                    flag = True
                    return True

            if flag is False:

                if call(["git", "branch"], stderr = STDOUT, stdout = open(os.devnull, "w")) != 0:
                    return False

                else:
                    os.system("git pull")
                    return True

    except:
        return False


"""
PySQL
Devansh Singh, 2020
"""
