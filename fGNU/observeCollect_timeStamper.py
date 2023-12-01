from datetime import datetime
import os

class timeStamper:

	def returnDatetimeNowString(self):
		return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
		
	def returnFilePath(self,appendDate):
		dataPath = os.path.join(os.environ['GBOPARENTPATH'],"data",appendDate)
		return dataPath
