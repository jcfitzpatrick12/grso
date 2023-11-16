# general variables to change

import os

class sys_vars:
    def __init__(self):
        self.window_size=1024
        self.window_type = "blackmanharris"

        self.isAveraging = True
        self.averageOverInt = 2

        #the path to the file
        self.pathtoPdata = os.path.join(os.getcwd(),"Pdata")
    