# general variables to change

import os

class sys_vars:
    def __init__(self):
        self.window_size=1024
        self.window_type = "blackmanharris"
        self.averageOverInt = 10
        #the path to the data file
        self.path_to_data = os.path.join(os.environ['GBOPARENTPATH'],"data")

        #default time format
        self.default_time_format="%Y-%m-%dT%H:%M:%S"

    