from datetime import datetime
import os
from fMisc.sys_vars import sys_vars


class TimeStamper:
	def return_time_now_as_string(self):
		return datetime.now().strftime(sys_vars().default_time_format)
	def return_temp_file_path(self,pseudo_start_time):
		data_path = os.path.join(os.environ['GRSOPARENTPATH'],"temp_data",pseudo_start_time)
		return data_path
