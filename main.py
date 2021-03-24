"""
module for running
PySQL Python Wrapper CLI
"""

try:
    import packages.ddl_commands as ddl
    import packages.dml_commands as dml

except:
    raise Exception("Package Error: Contact Admin")


"""
PySQL
Devansh Singh, 2021
"""