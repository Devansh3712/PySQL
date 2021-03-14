"""
module for data-manipulation
language based commands
"""

try:
    import mysql.connector as mc

except:
    raise Exception("'dml_commands' module not setup")
