# this module will be imported in the into your flowgraph
import pmt

def to_pmt(value):
	# Map Python types to PMT conversion functions
	type_map = {
		int: pmt.from_long,
		float: pmt.from_double,
		str: pmt.intern,
		bool: pmt.from_bool,
	}
	# Get the PMT conversion function based on the value's type
	converter = type_map.get(type(value))
	if converter:
		return converter(value)
	else:
		raise ValueError(f"Unsupported type: {type(value)}")

def get_dict(**kwargs):
	pmt_dict = pmt.make_dict()
	# Iterate over keyword arguments and add to the PMT dictionary
	for key, value in kwargs.items():
		pmt_key = pmt.intern(key)
		pmt_value = to_pmt(value)
		pmt_dict = pmt.dict_add(pmt_dict, pmt_key, pmt_value)
	return pmt_dict
