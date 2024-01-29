# this module will be imported in the into your flowgraph
import pmt

class BuildDict:
	def __init__(self):
		self.pmt_dict = pmt.make_dict()

	# Define a function to convert Python types to PMT types
	def to_pmt(self,value):
		if isinstance(value, int):
			return pmt.from_long(value)
		elif isinstance(value, float):
			return pmt.from_double(value)
		elif isinstance(value, str):
			return pmt.intern(value)
		elif isinstance(value, bool):
			return pmt.from_bool(value)
		# Add more type conversions here if needed
		else:
			raise ValueError(f"Unsupported type: {type(value)}")



	def GetDict(self,samp_rate,center_freq,chunk_start_time):
		# Define a list of key-value pairs with different types
		key_value_pairs = [
		('samp_rate', int(samp_rate)),
		('center_freq', float(center_freq)),
		('chunk_start_time', chunk_start_time),
		# Add more key-value pairs here
		]
		# Add key-value pairs to the PMT dictionary
		for key, value in key_value_pairs:
			pmt_key = pmt.intern(key)
			pmt_value = self.to_pmt(value)
			self.pmt_dict = pmt.dict_add(self.pmt_dict, pmt_key, pmt_value)
		
		return self.pmt_dict
