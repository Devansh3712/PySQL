from setuptools import *
from os import path

with open ("requirements.txt") as f:
    requirements = f.readlines()

this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, "README.md"), encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name = "pysql-cli",
    version = "1.0.2",
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
