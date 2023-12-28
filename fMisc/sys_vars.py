# general variables to change

import os
from datetime import datetime

class sys_vars:
    def __init__(self):
        self.window_size=1024
        self.window_type = "blackmanharris"
        self.average_over_int = 10
        
        self.default_time_format="%Y-%m-%dT%H:%M:%S"
        #the path to the data file
        self.path_to_data = os.path.join(os.environ['GRSOPARENTPATH'],"data")
        self.path_to_temp_data = os.path.join(os.environ['GRSOPARENTPATH'],"temp_data")
        #default time format









    