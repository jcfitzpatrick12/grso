#!/bin/bash


# Define the base URL
base_url="https://www.astro.gla.ac.uk/users/eduard/callisto"

# Function to validate numeric input
is_numeric() {
    [[ $1 =~ ^[0-9]+$ ]]
}

# Prompt user for year (YYYY)
while true; do
    read -p "Enter year (YYYY): " year
    if is_numeric "$year" && [ ${#year} -eq 4 ]; then
        break
    else
        echo "Invalid input for year. Please ensure it is a four-digit number."
    fi
done

# Prompt user for month (MM)
while true; do
    read -p "Enter month (MM): " month
    if is_numeric "$month" && [ "$month" -ge 1 ] && [ "$month" -le 12 ]; then
        month=$(printf "%02d" $month)  # Format to two digits
        break
    else
        echo "Invalid input for month. Please enter a number between 01 and 12."
    fi
done

# Prompt user for day (DD)
while true; do
    read -p "Enter day (DD): " day
    if is_numeric "$day" && [ "$day" -ge 1 ] && [ "$day" -le 31 ]; then  # Basic range check, not accounting for month-specific days
        day=$(printf "%02d" $day)  # Format to two digits
        break
    else
        echo "Invalid input for day. Please enter a number between 01 and 31."
    fi
done

# Construct `date_dir` and `data_dir` paths
date_dir="$year/$month/$day"
data_dir="data/$date_dir"
data_path="$GRSOPARENTPATH/$data_dir"
bash src/monitor/create_dir.sh $data_path

# Build the URL for the day
url="${base_url}/${year}/${month}/${day}/"

# Use wget to download all .fit files from the directory for the specified day
# -r: recursive, -l1: one level deep (no recursion), -np: no parent, -nd: no directories, -A: accepted extensions
wget -r -l1 -np -nd -A .fit -P "${data_path}" "${url}"

# Note: Replace "path/to/destination/folder" with the actual path where you want to save the files.
python3 ./standardise_file_names.py