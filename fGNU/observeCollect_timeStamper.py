from datetime import datetime
import os

class timeStamper:

	def returnDatetimeNowString(self):
		return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
		
	def returnFilePath(self,appendDate):
		data_path = os.path.join(os.environ['GRSOPARENTPATH'],"temp_data",appendDate)
		return data_path
