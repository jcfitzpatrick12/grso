import os


homebrew_tags = ["00", "02", "03"]
reserved_tags = ["01"]
defined_tags = homebrew_tags + reserved_tags

default_time_format = "%Y-%m-%dT%H:%M:%S"
glasgow_callisto_time_format = "GLASGOW_%Y%m%d_%H%M%S_01"


path_to_data = os.path.join(os.environ['GRSOPARENTPATH'],"data")
path_to_temp_data = os.path.join(os.environ['GRSOPARENTPATH'],"temp_data")
path_to_figures = os.path.join(os.environ['GRSOPARENTPATH'],"figures")
path_to_config_data = os.path.join(os.environ['GRSOPARENTPATH'],"config_data")