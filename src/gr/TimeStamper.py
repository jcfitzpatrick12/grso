from datetime import datetime
import os
from src.configs import GLOBAL_CONFIG


def return_time_now_as_string():
	return datetime.now().strftime(GLOBAL_CONFIG.default_time_format)


def return_temp_file_path(chunk_start_time, tag):
	data_path = os.path.join(os.environ['GRSOPARENTPATH'],"temp_data",f"{chunk_start_time}_{tag}")
	return data_path
