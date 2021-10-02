from setuptools import *
from os import path

this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, "README.md"), encoding = "utf-8") as file:
    long_description = file.read()

with open(path.join(this_dir, "requirements.txt"), encoding = "utf-8") as file:
    requirements = file.readlines()

setup(
    name = "pysql-cli",
    version = "1.1.2",
    author = "Devansh Singh",
    author_email = "devanshamity@gmail.com",
    url = "https://github.com/Devansh3712/PySQL",
    description = "CLI for making MySQL queries easier",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "MIT",
    packages = find_packages(),
    include_package_data = True,
    entry_points = {
        "console_scripts": [
            "pysql=pysql.main:cli",
            "cpysql=pysql.main_c:cli"
        ]
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = requirements,
)

"""
PySQL
Devansh Singh, 2021
"""
