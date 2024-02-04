import os
import re

from src.configs import GLOBAL_CONFIG
from src.utils import DatetimeFuncs
from datetime import datetime 

def file_describes_callisto_data(s):
    # Adjust the regex pattern to match the new format with "_01" at the end
    pattern = re.compile(r'^GLASGOW_\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}_01$')
    
    # Use the pattern to search the string
    if pattern.match(s):
        # Attempt to parse the date to ensure it's valid, ignoring the "_01" suffix
        try:
            datetime.strptime(s[8:-3], "%Y%m%d_%H%M%S")
            return True
        except ValueError:
            # The datetime part is not a valid date/time
            return False
    else:
        # The string does not match the pattern
        return False

def main():
#walk through all the subdirectories in data
    for root, dirs, files in os.walk(GLOBAL_CONFIG.path_to_data):
        for file in files:
            current_path = os.path.join(root, file)
            name, ext = os.path.splitext(file)
            if file_describes_callisto_data(name):
                try:
                    new_name = DatetimeFuncs.transform_time_format(name, GLOBAL_CONFIG.glasgow_callisto_time_format, GLOBAL_CONFIG.default_time_format)
                except Exception as e:
                    print(f"Could not transform file name to standard format! For file named {name}, received the error {e}")
                new_path = os.path.join(root, f"{new_name}_01.fits")
                os.rename(current_path, new_path)


if __name__=="__main__":
    main()
    exit()