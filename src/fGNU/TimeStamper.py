from datetime import datetime
import os
from src.fConfig import CONFIG


class TimeStamper:
	def return_time_now_as_string(self):
		return datetime.now().strftime(CONFIG.default_time_format)
	def return_temp_file_path(self,chunk_start_time):
		data_path = os.path.join(os.environ['GRSOPARENTPATH'],"temp_data",f"{chunk_start_time}_00")
		return data_path
