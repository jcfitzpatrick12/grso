#!/bin/bash

# Define the date you want to fetch data for in YYYYMMDD format
date="20240129"

# Define the base URL
base_url="https://www.astro.gla.ac.uk/users/eduard/callisto"


# Instead of using the current date, use the defined `date` variable to set `date_dir`
year=${date:0:4}
month=${date:4:2}
day=${date:6:2}

# Construct `date_dir` using the extracted year, month, and day
date_dir="$year/$month/$day"
data_dir="data/$date_dir"
data_path="$GRSOPARENTPATH/$data_dir"
bash src/fMonitor/create_dir.sh $data_path


# Extract year, month, day for URL construction
year=${date:0:4}
month=${date:4:2}
day=${date:6:2}

# Build the URL for the day
url="${base_url}/${year}/${month}/${day}/"

# Use wget to download all .fit files from the directory for the specified day
# -r: recursive, -l1: one level deep (no recursion), -np: no parent, -nd: no directories, -A: accepted extensions
wget -r -l1 -np -nd -A .fit -P "${data_path}" "${url}"

# Note: Replace "path/to/destination/folder" with the actual path where you want to save the files.
python3 src/fCallisto/standardise_file_names.py