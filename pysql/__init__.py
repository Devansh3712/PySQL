"""
module for PySQL wrapper
functions, for using as a
library
"""

__author__ = "Devansh Singh"
__email__ = "devanshamity@gmail.com"
__license__ = "MIT"

from pysql import *

"""
classes for functions

for initializing object instances,
use (username, password) of
local MySQL server
"""

from pysql.packages.auth import Database
from pysql.packages.ddl_commands import DDL, Alter
from pysql.packages.dml_commands import DML
from pysql.data.export import Export
from pysql.data.imports import Import

"""
PySQL
Devansh Singh, 2021
"""
