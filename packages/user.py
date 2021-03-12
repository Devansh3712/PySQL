'''
module for user authentication
'''

import mysql.connector as mc

#class for maintaining user credentials
class Database:
    
    def __init__(self, username: str, password: str):
        self.uname = username
        self.passw = password

    #authentication of provided credentials
    def authenticate(self) -> bool:

        try:
            #initialize connection with MySQL
            self.connection = mc.connect(host = "localhost", user = f"{self.uname}", password = f"{self.passw}")

            if (self.connection.is_connected()):
                #initialize cursor object for operation
                self.cursor = self.connection.cursor(buffered = True)
                return True

            else:
                return False

        except:
            return False